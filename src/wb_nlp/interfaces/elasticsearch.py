from datetime import datetime
import re
from pathlib import Path
import elasticsearch_dsl
import pandas as pd

# from elasticsearch import helpers
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan
from elasticsearch.exceptions import ConnectionTimeout

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Object, Nested, A, Boolean
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet, NestedFacet
from elasticsearch_dsl.query import MultiMatch, Match, Term
from wb_cleaning.extraction import country_extractor, jdc_tags_extractor

from wb_nlp.dir_manager import get_path_from_root

connections.create_connection(hosts=['es01'])


_ES_CLIENT = None
DOC_INDEX = "nlp-documents"
DOC_TOPIC_INDEX = "nlp-doc-topics"


def get_client():
    global _ES_CLIENT
    if _ES_CLIENT is None:
        _ES_CLIENT = Elasticsearch(
            hosts=[{"host": "es01", "port": 9200}], timeout=30, max_retries=5, retry_on_timeout=True)

    return _ES_CLIENT


class NLPDoc(Document):
    # Add tags here for different applications
    app_tag_jdc = Boolean()

    id = Keyword()
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    app_tags = Keyword()
    body = Text(analyzer='snowball')
    abstract = Text(analyzer='snowball')
    adm_region = Keyword()
    author = Keyword()
    country = Keyword()
    corpus = Keyword()
    date_published = Date()
    der_countries = Object()
    der_country_details = Nested(properties={"code": Keyword(), "count": Integer(
    ), "name": Keyword(), "region": Keyword(), "sub-region": Keyword()})
    der_regions = Keyword()
    der_sub_regions = Keyword()
    der_intermediate_regions = Keyword()
    der_country_groups = Keyword()
    der_jdc_data = Nested(properties={"tag": Keyword(), "count": Integer()})
    der_jdc_tags = Keyword()
    doc_type = Keyword()
    geo_region = Keyword()
    last_update_date = Date()
    major_doc_type = Keyword()
    wb_subtopic_src = Keyword()
    topics_src = Keyword()
    year = Integer()
    tokens = Integer()
    views = Integer()

    class Index:
        name = DOC_INDEX
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 1,
            "highlight": {"max_analyzed_offset": 5000000},
            "max_terms_count": 262144,  # 2 ^ 18
            "refresh_interval": "30s"
        }

    def save(self, **kwargs):
        # Set all application tags to False first
        # Then just use the tag updated script to set the True values
        self.app_tag_jdc = False

        self.tokens = len(self.body.split())
        self.views = 0

        # Extract JDC specific tags
        self.der_jdc_data = jdc_tags_extractor.get_jdc_tag_counts(self.body)
        self.der_jdc_tags = [i["tag"] for i in self.der_jdc_data]

        # Extract country mentions data
        country_counts = country_extractor.get_country_counts(self.body)

        country_groups = []
        if self.country is not None:
            for c in self.country:
                code = country_extractor.get_country_code_from_name(c)
                g = country_extractor.country_code_country_group_map.get(code)
                if g:
                    country_groups.extend(g)

        self.der_country_groups = country_groups

        self.der_countries = country_counts
        self.der_country_details = country_extractor.get_country_count_details(
            country_counts)

        return super(NLPDoc, self).save(**kwargs)

    def structure_stats_by_year_data(self, data, round_size=None):
        year_buckets = data["year"]["buckets"]
        country_total = {}
        records = []

        by_year = {}

        for year_bucket in year_buckets:
            year_data = []
            year = year_bucket["key_as_string"].split("T")[0]
            year_doc_count = year_bucket["doc_count"]
            year_unique_countries = year_bucket["root"]["doc_count"]

            for d in year_bucket["root"]["code"]["buckets"]:
                t = d.pop("total")
                d.update(t)
                d["year"] = year
                d["year_doc_count"] = year_doc_count
                d["year_unique_countries"] = year_unique_countries

                if round_size is not None:
                    d["value"] = round(d["value"], round_size)

                country_total[d["key"]] = country_total.get(
                    d["key"], 0) + d["value"]
                d["cumulative_value"] = country_total[d["key"]]

                year_data.append(d)

            by_year[year] = {v["key"]: v["value"] for v in year_data}
            records.extend(year_data)

        return dict(
            records=records,
            year=by_year)

    def get_country_counts(self):
        s = self.search()

        root = A("nested", path="der_country_details")
        code = A("terms", field="der_country_details.code", size=1000)
        total = A("sum", field="der_country_details.count")

        s.aggs.bucket("root", root).bucket("code", code).bucket("total", total)

        return s.execute().aggregations.to_dict()

    def get_country_counts_by_year(self, filters=None):
        search = self.search()

        if filters:
            for f in filters:
                for ftype, fvalue in f.items():
                    search = search.filter(ftype, **fvalue)

        year = A("date_histogram",
                 field="date_published",
                 calendar_interval="year")

        root = A("nested", path="der_country_details")
        code = A("terms", field="der_country_details.code", size=1000)
        total = A("sum", field="der_country_details.count")

        search.aggs.bucket("year", year).bucket("root", root).bucket(
            "code", code).bucket("total", total)

        return self.structure_stats_by_year_data(search.execute().aggregations.to_dict())

    def get_country_share_by_year(self, filters=None):
        search = self.search()

        if filters:
            for f in filters:
                for ftype, fvalue in f.items():
                    search = search.filter(ftype, **fvalue)

        year = A("date_histogram",
                 field="date_published",
                 calendar_interval="year")

        root = A("nested", path="der_country_details")
        code = A("terms", field="der_country_details.code", size=1000)
        total = A("sum", field="der_country_details.percent")

        search.aggs.bucket("year", year).bucket("root", root).bucket(
            "code", code).bucket("total", total)

        return self.structure_stats_by_year_data(search.execute().aggregations.to_dict(), round_size=4)


class DocTopic(Document):
    # _id=f"{self.model_run_info['model_run_info_id']}-{doc_id}",
    id = Keyword()
    topics = Object()
    model_run_info_id = Keyword()

    adm_region = Keyword()
    country = Keyword()
    corpus = Keyword()
    date_published = Date()
    doc_type = Keyword()
    geo_region = Keyword()
    major_doc_type = Keyword()
    topics_src = Keyword()
    year = Integer()

    # Add tags here for different applications
    app_tag_jdc = Boolean()

    class Index:
        name = DOC_TOPIC_INDEX
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 1,
            "max_terms_count": 262144,  # 2 ^ 18
            "refresh_interval": "30s"
        }

    def save(self, **kwargs):
        return super(DocTopic, self).save(**kwargs)


try:
    NLPDoc.init()
    DocTopic.init()
except exceptions.ConnectionError:
    pass
except exceptions.RequestError:
    print("Warning: RequestError. A re-index may be required.")


class NLPDocFacetedSearch(FacetedSearch):
    # doc_types = [elasticsearch.NLPDoc, ]
    index = DOC_INDEX
    doc_types = [NLPDoc]

    # fields that should be searched
    fields = ['title^5', 'body^1.25', 'abstract^1.5', 'author', 'country']

    facets = {
        # use bucket aggregations to define facets
        'author': TermsFacet(field='author', size=100),
        'country': TermsFacet(field='country', size=100),
        'der_country_groups': TermsFacet(field='der_country_groups', size=100),
        'der_country_details_region': NestedFacet("der_country_details", TermsFacet(field='der_country_details.region', size=100, metric=A("value_count", field='id'))),
        'der_jdc_tags': TermsFacet(field='der_jdc_tags', size=100),
        'corpus': TermsFacet(field='corpus', size=100),
        'major_doc_type': TermsFacet(field='major_doc_type', size=100),
        'adm_region': TermsFacet(field='adm_region', size=100),
        'geo_region': TermsFacet(field='geo_region', size=100),
        'topics_src': TermsFacet(field='topics_src', size=100),
        'year': DateHistogramFacet(field='date_published', calendar_interval='year')
    }

    def search(self):
        search = super().search()
        search = search.extra(track_total_hits=True)
        search = search.source(excludes=["body", "doc"])
        # search.params(preserve_order=True).scan()
        return search

    def build_search(self):
        """
        Construct the ``Search`` object.
        """
        s = self.search()
        s = self.query(s, self._query)
        s = self.filter(s)
        if self.fields:
            s = self.highlight(s)
        s = self.sort(s)
        self.aggregate(s)

        # # Region aggregation from nested field
        d = {
            "query": {
                "match_all": {}
            },
            "aggs": {
                "der_country_details": {
                    "nested": {
                        "path": "der_country_details"
                    },
                    "aggs": {
                        "top_regions": {
                            "terms": {
                                "field": "der_country_details.region"
                            },
                            "aggs": {
                                "region_to_doc": {
                                    "reverse_nested": {},
                                    "aggs": {
                                        "doc_count_per_region": {
                                            "value_count": {
                                                "field": "id"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        query = s.to_dict()
        query['aggs']['_filter_der_country_details_region']['aggs'] = d['aggs']

        # `from_dict` will not have the index and doc_type properties so it will search for all the indices available.
        # Since we are just interested in updating the aggregation, we can just create a new search object from the dict
        # and override the aggs attribute of the original search object that actually index- and doc_type-aware.

        search = Search.from_dict(query)
        s.aggs = search.aggs

        return s


class JDCNLPDocFacetedSearch(FacetedSearch):
    # doc_types = [elasticsearch.NLPDoc, ]
    index = DOC_INDEX
    doc_types = [NLPDoc]

    # fields that should be searched
    fields = ['title^5', 'body^1.25', 'abstract^1.5', 'author', 'country']

    facets = {
        # use bucket aggregations to define facets
        'author': TermsFacet(field='author', size=100),
        'country': TermsFacet(field='country', size=100),
        'der_country_groups': TermsFacet(field='der_country_groups', size=100),
        'der_jdc_tags': TermsFacet(field='der_jdc_tags', size=100),
        'corpus': TermsFacet(field='corpus', size=100),
        'major_doc_type': TermsFacet(field='major_doc_type', size=100),
        'adm_region': TermsFacet(field='adm_region', size=100),
        'geo_region': TermsFacet(field='geo_region', size=100),
        'topics_src': TermsFacet(field='topics_src', size=100),
        'year': DateHistogramFacet(field='date_published', calendar_interval='year')
    }

    def search(self):
        search = super().search()
        search = search.extra(track_total_hits=True)
        search = search.source(excludes=["body", "doc"])
        # search.params(preserve_order=True).scan()

        search = search.filter("term", app_tag_jdc=True)

        return search


def get_indexed_corpus_size(filters=None):

    search = NLPDoc.search()

    if filters:
        for f in filters:
            for ftype, fvalue in f.items():
                search = search.filter(ftype, **fvalue)

    return search.count()


def store_docs_topics(doc_ids, vectors, model_run_info_id, metadata=None, ignore_existing=True):
    '''
    metadata: dict {id: {field: value, ...}}
    '''
    existing_ids = set()

    if ignore_existing:
        existing_ids = get_ids(index=DocTopic.Index.name)

    for ix, (doc_id, topic_list) in enumerate(zip(doc_ids, vectors)):
        if ix and ix % 10000 == 0:
            print(ix)

        topics = {f"topic_{topic_id}": value for topic_id,
                  value in enumerate(topic_list)}

        es_id = f"{model_run_info_id}-{doc_id}"

        if es_id in existing_ids:
            continue

        store_doc_topics(
            es_id=es_id,
            doc_id=doc_id,
            topics=topics,
            model_run_info_id=model_run_info_id,
            metadata=metadata.get(doc_id))


def store_doc_topics(es_id, doc_id, topics, model_run_info_id, metadata=None):
    _id = f"{model_run_info_id}-{doc_id}"
    assert es_id == _id

    data = dict(
        id=doc_id,
        topics=topics,
        model_run_info_id=model_run_info_id,
    )
    if metadata is not None:
        data.update(metadata)

    topic_doc = DocTopic(meta={'id': es_id}, **data)
    topic_doc.save()


def get_connections():
    return connections


def get_ids(index=None):
    if index is None:
        index = NLPDoc.Index.name

    existing_ids = {obj["_id"] for obj in scan(get_client(), query=dict(
        query=dict(match_all={}),
        _source=False),
        size=5000,
        index=index)}

    return existing_ids


def get_ids_from_query(doc_index, query=None, ids_only=True):
    # doc_index: NLPDoc, DocTopic, etc.

    index = doc_index.Index.name

    search_query = {}

    if query is None:
        search_query["query"] = dict(match_all={})
    else:
        search_query["query"] = query

    if ids_only:
        search_query["_source"] = ["id"]

    existing_ids = {obj["_source"]["id"] for obj in scan(get_client(), query=search_query,
                                                         size=5000,
                                                         index=index)}

    return list(existing_ids)


def get_metadata_by_ids(doc_ids, index=None, source=None, source_includes=None, source_excludes=None):
    '''
    This method returns the metadata corresponding to the list of ids in `doc_ids`.
    The source input parametrize the return value for the _source field.
        source = False                          : Don't return any
        source = []                             : Return all values in the _source
        source = dict(excludes=["body"])        : Return all values except the body.
    '''
    if index is None:
        index = NLPDoc.Index.name

    if source is False:
        pass
    elif source is None:
        source = {}
        if source_excludes:
            source["excludes"] = source_excludes
        if source_includes:
            source["includes"] = source_includes
    elif isinstance(source, list):
        _source = {}
        if source_excludes:
            _source["excludes"] = source_excludes
        if source_includes:
            _source["includes"] = sorted(set(source + source_includes))
        source = _source
    elif isinstance(source, dict):
        if source_excludes:
            source["excludes"] = sorted(
                set(source_excludes + source.get("excludes", [])))
        if source_includes:
            source["includes"] = sorted(
                set(source_includes + source.get("includes", [])))

    return [obj["_source"] for obj in scan(
        get_client(),
        query=dict(
            query=dict(terms={"_id": doc_ids}),
            _source=source),
        size=len(doc_ids),
        index=index)]


def make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True, en_txt_only=True, remove_doc_whitespaces=True, log_freq_rate=25):
    # from elasticsearch_dsl import Index
    # i = Index(name=elasticsearch.DOC_INDEX, using=elasticsearch.get_client())
    # i.delete()
    # from wb_nlp.interfaces import elasticsearch, mongodb
    # docs_metadata_coll = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = list(docs_metadata_coll.find({}))
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True, en_txt_only=True, remove_doc_whitespaces=True)
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=False, en_txt_only=True, remove_doc_whitespaces=True)

    # test_docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    docs_count = len(docs_metadata)
    log_freq = docs_count // log_freq_rate

    existing_ids = set()

    if ignore_existing:
        existing_ids = get_ids(index=NLPDoc.Index.name)

        # for obj in scan(get_client(), query=dict(
        #         query=dict(match_all={}),
        #         fields=["_id"]),
        #         size=5000,
        #         index=NLPDoc.Index.name):
        #     existing_ids.add(obj["_id"])

    root_path = Path(get_path_from_root())

    for ix, data in enumerate(docs_metadata):
        doc_path = root_path / data["path_original"]
        # doc_path = doc_path.parent / "TXT_ORIG" / doc_path.name
        en_doc_path = doc_path.parent.parent / "EN_TXT_ORIG" / doc_path.name

        if ix and ix % log_freq == 0:
            print(f"Processed {ix} of {docs_count} docs...")

        if en_txt_only and not en_doc_path.exists():
            continue

        if data["_id"] in existing_ids:
            continue

        if not doc_path.exists():
            continue

        # create and save and article
        nlp_doc = NLPDoc(meta={'id': data["_id"]}, **data)

        with open(doc_path, 'rb') as open_file:
            doc = open_file.read().decode('utf-8', errors='ignore')
            if remove_doc_whitespaces:
                doc = re.sub(r"\s+", " ", doc)
            nlp_doc.body = doc

        try:
            nlp_doc.save()
        except ConnectionTimeout:
            try:
                nlp_doc.save()
            except ConnectionTimeout:
                nlp_doc.save()


def faceted_search_nlp_docs():
    ns = NLPDocFacetedSearch()
    # ns = elasticsearch.NLPDocFacetedSearch("poor", {"countries": ["Indonesia", "Brazil"]})
    response = ns.execute()

    for hit in response:
        print(hit.meta.score, hit.title)

    for (country, count, selected) in response.facets.countries:
        print(country, ' (SELECTED):' if selected else ':', count)

    # for (year, count, selected) in response.facets.publishing_frequency:
    #     print(year.strftime('%Y'), ' (SELECTED):' if selected else ':', count)


def common_search(query, from_result=0, size=10, return_body=False, ignore_cache=False, return_highlights=True, highlight_field="body", fragment_size=100):
    """
    query: DSL query
    """
    search = NLPDoc.search()
    search = search.query(query)
    search = search.extra(track_total_hits=True)

    if return_highlights:
        search = search.highlight_options(order="score")
        search = search.highlight(
            highlight_field, fragment_size=fragment_size)

    search = search[from_result: from_result + size]

    if not return_body:
        search = search.source(excludes=["body", "doc"])

    response = search.execute(ignore_cache=ignore_cache)

    return response


def text_search(query, from_result=0, size=10, return_body=False, ignore_cache=False, return_highlights=True, highlight_field="body", fragment_size=100):
    query = MultiMatch(query=query, fields=[
                       "title", "body", "author", "abstract"])

    return common_search(
        query,
        from_result=from_result,
        size=size,
        return_body=return_body,
        ignore_cache=ignore_cache,
        return_highlights=return_highlights,
        highlight_field=highlight_field,
        fragment_size=fragment_size)


def author_search(query, from_result=0, size=10, return_body=False, ignore_cache=False, return_highlights=False, highlight_field="author", fragment_size=100):
    query = Term(query=query, fields=["author"])

    return common_search(
        query,
        from_result=from_result,
        size=size,
        return_body=return_body,
        ignore_cache=ignore_cache,
        return_highlights=return_highlights,
        highlight_field=highlight_field,
        fragment_size=fragment_size)


def ids_search(ids, query, from_result=0, size=10, return_body=False, ignore_cache=False, fragment_size=100):
    # query = MultiMatch(query=query, fields=["title", "body"])

    search = NLPDoc.search()
    search = search.filter("ids", values=ids)

    # search = search.query(query)

    search = search[from_result: from_result + size]

    # search = search.highlight_options(order="score")
    # search = search.highlight(
    #     "body", fragment_size=fragment_size)

    if not return_body:
        search = search.source(excludes=["body", "doc"])

    response = search.execute(ignore_cache=ignore_cache)

    return response


def update_doc_topic_metadata(docs_metadata):
    fields = [
        "adm_region", "country", "corpus", "date_published",
        "doc_type", "geo_region", "major_doc_type", "topics_src",
        "year"
    ]

    for ix, doc in enumerate(docs_metadata):
        if ix and ix % 1000 == 0:
            print(ix)

        search = DocTopic.search().filter("term", id=doc["id"])
        metadata = {k: doc.get(k) for k in fields}

        for hit in search.execute():
            hit.update(**metadata)


# for dobj in scan(es, query={"query": {"match_all": {}}, "fields": []}, size=10000, index="nlp-documents", doc_type=elasticsearch.NLPDoc):

# def timeseries_aggregations():
#     search = NLPDoc.search()
#     search.aggs.bucket(
#         "docs_per_year", "terms", field="year").bucket("docs_per_doc_type", "terms",  field="major_doc_type").metric("total_tokens", "sum", field="tokens")


class NLPDocAggregations:
    def __init__(self, doc_class=None):
        self.doc_class = doc_class or NLPDoc

    def get_search_aggregation(self, field, filters=None, return_ids=False):
        search = self.doc_class.search()

        if filters:
            for f in filters:
                for ftype, fvalue in f.items():
                    search = search.filter(ftype, **fvalue)

        if return_ids:
            search.aggs.bucket(
                "docs_per_year",
                "date_histogram",
                field="date_published",
                calendar_interval="year"
            ).metric(
                "year_total_tokens", "sum",
                field="tokens"
            ).bucket(
                f"docs_per_{field}",
                "terms",
                field=field,
                size=999999999
            ).metric(
                f"{field}_total_tokens", "sum",
                field="tokens"
            ).bucket(
                "ids", "terms",
                field="id", size=999999999)
        else:

            search.aggs.bucket(
                "docs_per_year",
                "date_histogram",
                field="date_published",
                calendar_interval="year"
            ).metric(
                "year_total_tokens", "sum",
                field="tokens"
            ).bucket(
                f"docs_per_{field}",
                "terms",
                field=field,
                size=999999999
            ).metric(
                f"{field}_total_tokens", "sum",
                field="tokens"
            )

        return search.execute()

    def get_doc_counts_by_year_by_field(self, field, filters=None, return_ids=False):
        result = self.get_search_aggregation(
            field=field, filters=filters, return_ids=return_ids)
        data = []

        for year_bucket in result.aggregations["docs_per_year"]["buckets"]:
            for field_bucket in year_bucket[f"docs_per_{field}"]["buckets"]:
                d = {
                    "year": year_bucket["key_as_string"].split("T")[0],
                    "year_doc_count": year_bucket["doc_count"],
                    "year_total_tokens": year_bucket["year_total_tokens"]["value"],
                    f"{field}": field_bucket["key"],
                    f"{field}_doc_count": field_bucket["doc_count"],
                    f"{field}_total_tokens": field_bucket[
                        f"{field}_total_tokens"]["value"],
                }

                if return_ids:
                    d["doc_ids"] = [i["key"]
                                    for i in field_bucket["ids"]["buckets"]]

                data.append(d)

        return data

    def get_doc_counts_by_year_by_major_doc_type(self, filters=None, return_ids=False):
        return self.get_doc_counts_by_year_by_field(field="major_doc_type", filters=filters, return_ids=return_ids)

    def get_doc_counts_by_year_by_adm_region(self, filters=None, return_ids=False):
        return self.get_doc_counts_by_year_by_field(field="adm_region", filters=filters, return_ids=return_ids)


class DocTopicAggregations:
    def __init__(self, model_id, doc_class=None):
        self.doc_class = doc_class or DocTopic
        self.model_id = model_id

    def get_topic_aggregation(self, field, topic, filters=None, return_ids=False):
        search = self.doc_class.search().filter("term", model_run_info_id=self.model_id)

        if filters:
            for f in filters:
                for ftype, fvalue in f.items():
                    search = search.filter(ftype, **fvalue)

        if return_ids:
            search.aggs.bucket(
                "topic_per_year",
                "date_histogram",
                field="date_published",
                calendar_interval="year"
            ).metric(
                "year_topic_sum", "sum",
                field=f"topics.{topic}"
            ).bucket(
                f"topic_per_{field}",
                "terms",
                field=field,
                size=999999999
            ).metric(
                f"{field}_topic_sum", "sum",
                field=f"topics.{topic}"
            ).bucket(
                "ids", "terms",
                field="id", size=999999999)
        else:
            search.aggs.bucket(
                "topic_per_year",
                "date_histogram",
                field="date_published",
                calendar_interval="year"
            ).metric(
                "year_topic_sum", "sum",
                field=f"topics.{topic}"
            ).bucket(
                f"topic_per_{field}",
                "terms",
                field=field,
                size=999999999
            ).metric(
                f"{field}_topic_sum", "sum",
                field=f"topics.{topic}"
            )

        return search.execute()

    def get_topic_profile_by_year_by_field(self, field, topic, filters=None, return_ids=False):
        result = self.get_topic_aggregation(
            field=field, topic=topic, filters=filters, return_ids=return_ids)
        data = []

        for year_bucket in result.aggregations["topic_per_year"]["buckets"]:
            for field_bucket in year_bucket[f"topic_per_{field}"]["buckets"]:
                d = {
                    "topic": topic,
                    "year": year_bucket["key_as_string"].split("T")[0],
                    "year_doc_count": year_bucket["doc_count"],
                    "year_topic_sum": year_bucket["year_topic_sum"]["value"],
                    f"{field}": field_bucket["key"],
                    f"{field}_doc_count": field_bucket["doc_count"],
                    f"{field}_topic_sum": field_bucket[
                        f"{field}_topic_sum"]["value"],
                }

                if return_ids:
                    d["doc_ids"] = [i["key"]
                                    for i in field_bucket["ids"]["buckets"]]

                data.append(d)

        return data

    def get_topic_profile_by_year_by_major_doc_type(self, topic, filters=None, return_ids=False):
        return self.get_topic_profile_by_year_by_field(field="major_doc_type", topic=topic, filters=filters, return_ids=return_ids)

    def get_topic_profile_by_year_by_adm_region(self, topic, filters=None, return_ids=False):
        return self.get_topic_profile_by_year_by_field(field="adm_region", topic=topic, filters=filters, return_ids=return_ids)


######################## JDC and TOPIC related helpers ########################

# def set_app_tag_jdc(ids):

#     for id in ids:
#         doc = NLPDoc.get(id)
#         doc.update(app_tag_jdc=True)

#     # Find documents that may have been tagged as a JDC doc
#     # but no longer qualify based on the new filter.
#     # Then set their tags to False.

#     search = NLPDoc.search()
#     search = search.exclude("ids", values=list(
#         ids)).filter("term", app_tag_jdc=True)
#     search_query = search.to_dict()

#     ids = get_ids_from_query(
#         NLPDoc, query=search_query["query"], ids_only=True)

#     for id in ids:
#         doc = NLPDoc.get(id)
#         doc.update(app_tag_jdc=False)

def set_app_tag_jdc_NLPDoc(ids):
    ids = list(ids)

    ubq = elasticsearch_dsl.UpdateByQuery(
        index=NLPDoc.Index.name, using=get_client())
    ubq = ubq.filter("terms", id=ids).exclude("term", app_tag_jdc=True)
    ubq = ubq.script(source="ctx._source.app_tag_jdc=true;")
    ubq = ubq.params(scroll_size=50).params(
        conflicts="proceed")  # .params(requests_per_second=10)

    print("Executing JDC tag addition in NLPDoc...")
    response = ubq.execute()
    print(response.to_dict())

    ubq = elasticsearch_dsl.UpdateByQuery(
        index=NLPDoc.Index.name, using=get_client())
    ubq = ubq.filter("term", app_tag_jdc=True).exclude("terms", id=ids)
    ubq = ubq.script(source="ctx._source.app_tag_jdc=false;")
    ubq = ubq.params(scroll_size=50).params(conflicts="proceed")

    print("Executing JDC tag removal in NLPDoc...")
    response = ubq.execute()
    print(response.to_dict())


def set_app_tag_jdc_DocTopic(ids):
    ids = list(ids)

    ubq = elasticsearch_dsl.UpdateByQuery(
        index=DocTopic.Index.name, using=get_client())
    ubq = ubq.filter("terms", id=ids).exclude("term", app_tag_jdc=True)
    ubq = ubq.script(source="ctx._source.app_tag_jdc=true;")
    ubq = ubq.params(scroll_size=50).params(conflicts="proceed")

    print("Executing JDC tag addition in DocTopic...")
    response = ubq.execute()
    print(response.to_dict())

    ubq = elasticsearch_dsl.UpdateByQuery(
        index=DocTopic.Index.name, using=get_client())
    ubq = ubq.filter("term", app_tag_jdc=True).exclude("terms", id=ids)
    ubq = ubq.script(source="ctx._source.app_tag_jdc=false;")
    ubq = ubq.params(scroll_size=50).params(conflicts="proceed")

    print("Executing JDC tag removal in DocTopic...")
    response = ubq.execute()
    print(response.to_dict())


def set_app_tag_jdc(ids):

    try:
        set_app_tag_jdc_NLPDoc(ids)
    except Exception as e:
        print(e)

    try:
        set_app_tag_jdc_DocTopic(ids)
    except Exception as e:
        print(e)


def get_topic_threshold_query(model_run_info_id, topic_percentage):
    """
    model_run_info_id: id of the topic model
    topic_percentage: dict => {topic_id: percentage (0-1)}
    """

    topic_filters = [dict(range={f"topics.topic_{id}": {"gte": val}})
                     for id, val in sorted(topic_percentage.items())]

    query = dict(bool=dict(
        must=[{"term": {"model_run_info_id": model_run_info_id}}] + topic_filters))

    return query


def get_jdc_docs_stats(ids):
    # docs = elasticsearch.NLPDoc.mget(ids)
    index = NLPDoc.Index.name

    search = NLPDoc.search()
    search = search.filter("ids", values=list(ids))
    search = search.filter(
        "terms", der_jdc_tags=[
            "asylum_seeker", "country_of_asylum", "internally_displaced_population",
            "refugee", "refugee_camp", "stateless"])

    search = search.source(includes=["id", "der_jdc_data", "major_doc_type"])

    search_query = search.to_dict()

    dataset = []
    for result in scan(get_client(), query=search_query,
                       size=5000,
                       index=index):

        data = result["_source"]

        dataset.append(
            dict(
                id=data["id"],
                total_words=sum(
                    [i["count"] for i in data["der_jdc_data"]]),
                num_tags=len(data["der_jdc_data"]),
                doc_type=data.get("major_doc_type", [None])[0])
        )

    return dataset


def get_topics_by_id(model_run_info_id, topic_ids, ids):
    # doc_index: NLPDoc, DocTopic, etc.

    index = DocTopic.Index.name

    ids_topic = [f"{model_run_info_id}-{i}" for i in ids]

    search = DocTopic.search()
    search = search.filter("term", model_run_info_id=model_run_info_id).filter(
        "ids", values=ids_topic)
    search = search.source(
        includes=["id"] + [f"topics.topic_{i}" for i in topic_ids])

    search_query = search.to_dict()

    dataset = []
    for result in scan(get_client(), query=search_query,
                       size=5000,
                       index=index):

        data = result["_source"]

        data.update(data.pop("topics"))
        dataset.append(data)

    return dataset


def get_topic_jdc_stats(model_run_info_id, topic_percentage):

    topic_ids = list(topic_percentage)

    print("Getting ids_by_topic")
    ids_by_topic = get_ids_from_query(DocTopic, query=get_topic_threshold_query(
        model_run_info_id, topic_percentage), ids_only=True)

    print("Getting ids_by_topic_with_tags")
    ids_by_topic_with_tags = get_ids_from_query(
        NLPDoc,
        query=NLPDoc.search().filter(
            "ids", values=list(ids_by_topic)).filter(
                "script", script="doc['der_jdc_tags'].length > 0").to_dict()["query"],
        ids_only=True)

    print("Getting get_jdc_docs_stats")
    jdc_doc_stats = get_jdc_docs_stats(ids_by_topic_with_tags)

    print("Getting get_topics_by_id")
    jdc_doc_topics = get_topics_by_id(
        model_run_info_id, topic_ids, ids_by_topic_with_tags)

    jdc_doc_stats = pd.DataFrame(jdc_doc_stats)
    jdc_doc_topics = pd.DataFrame(jdc_doc_topics)

    return jdc_doc_stats.merge(jdc_doc_topics, on="id")

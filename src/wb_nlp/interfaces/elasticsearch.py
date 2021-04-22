from datetime import datetime
import re
from pathlib import Path

# from elasticsearch import helpers
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Object, Nested, A
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from elasticsearch_dsl.query import MultiMatch, Match, Term
from wb_nlp.extraction import country_extractor
from wb_nlp.dir_manager import get_path_from_root

connections.create_connection(hosts=['es01'])


_ES_CLIENT = None
DOC_INDEX = "nlp-documents"
DOC_TOPIC_INDEX = "nlp-doc-topics"


def get_client():
    global _ES_CLIENT
    if _ES_CLIENT is None:
        _ES_CLIENT = Elasticsearch(hosts=[{"host": "es01", "port": 9200}])

    return _ES_CLIENT


class NLPDoc(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
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
    der_country_groups = Keyword()
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
            "highlight": {"max_analyzed_offset": 5000000}
        }

    def save(self, **kwargs):
        self.tokens = len(self.body.split())
        self.views = 0

        country_counts = country_extractor.get_country_counts(self.body)

        country_groups = []
        for c in self.country:
            g = country_extractor.country_country_group_map.get(c)
            if g:
                country_groups.extend(g)

        self.der_country_groups = country_groups

        self.der_countries = country_counts
        self.der_country_details = country_extractor.get_country_count_details(
            country_counts)
        return super(NLPDoc, self).save(**kwargs)

    def get_country_counts(self):
        s = self.search()

        root = A("nested", path="der_country_details")
        code = A("terms", field="der_country_details.code", size=1000)
        total = A("sum", field="der_country_details.count")

        s.aggs.bucket("root", root).bucket("code", code).bucket("total", total)

        return s.execute().aggregations.to_dict()


class DocTopic(Document):
    # _id=f"{self.model_run_info['model_run_info_id']}-{doc_id}",
    id = Keyword()
    topics = Object()
    model_run_info_id = Keyword()

    class Index:
        name = DOC_TOPIC_INDEX
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 1,
        }

    def save(self, **kwargs):
        return super(DocTopic, self).save(**kwargs)


try:
    NLPDoc.init()
    DocTopic.init()
except exceptions.ConnectionError:
    pass


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


def get_indexed_corpus_size():
    return NLPDoc.search().count()


def store_docs_topics(doc_ids, vectors, model_run_info_id, ignore_existing=True):
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
            model_run_info_id=model_run_info_id)


def store_doc_topics(es_id, doc_id, topics, model_run_info_id):
    _id = f"{model_run_info_id}-{doc_id}"
    assert es_id == _id

    data = dict(
        id=doc_id,
        topics=topics,
        model_run_info_id=model_run_info_id,
    )

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


def make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True, en_txt_only=True, remove_doc_whitespaces=True):
    # test_docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # elasticsearch.make_nlp_docs_from_docs_metadata(test_docs_metadata.find({}))
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

        if ix and ix % 10000 == 0:
            print(ix)

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


# for dobj in scan(es, query={"query": {"match_all": {}}, "fields": []}, size=10000, index="nlp-documents", doc_type=elasticsearch.NLPDoc):

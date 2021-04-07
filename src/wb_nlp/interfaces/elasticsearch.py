from datetime import datetime

from pathlib import Path

# from elasticsearch import helpers
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from elasticsearch_dsl.query import MultiMatch, Match

from wb_nlp.dir_manager import get_path_from_root

connections.create_connection(hosts=['es01'])


_ES_CLIENT = None
DOC_INDEX = "nlp-documents"


def get_client():
    global _ES_CLIENT
    if _ES_CLIENT is None:
        _ES_CLIENT = Elasticsearch(hosts=[{"host": "es01", "port": 9200}])

    return _ES_CLIENT


class NLPDoc(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    abstract = Text(analyzer='snowball')
    author = Keyword()
    country = Keyword()
    corpus = Keyword()
    date_published = Date()
    last_update_date = Date()
    year = Integer()
    tokens = Integer()
    views = Integer()

    class Index:
        name = DOC_INDEX
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 1,
        }

    def save(self, **kwargs):
        self.tokens = len(self.body.split())
        self.views = 0
        return super(NLPDoc, self).save(**kwargs)


try:
    NLPDoc.init()
except exceptions.ConnectionError:
    pass


class NLPDocFacetedSearch(FacetedSearch):
    # doc_types = [elasticsearch.NLPDoc, ]
    doc_types = [NLPDoc, ]
    # fields that should be searched
    fields = ['country', 'title', 'body']

    facets = {
        # use bucket aggregations to define facets
        'countries': TermsFacet(field='country'),
        'publishing_frequency': DateHistogramFacet(field='date_published', interval='year')
    }


def get_connections():
    return connections


def get_ids(index=None):
    if index is None:
        index = DOC_INDEX

    existing_ids = {obj["_id"] for obj in scan(get_client(), query=dict(
        query=dict(match_all={}),
        _source=False),
        size=5000,
        index=index)}

    return existing_ids


def get_metadata_by_ids(doc_ids, index=None, source_fields=None):
    if index is None:
        index = DOC_INDEX
    if source_fields is None:
        source_fields = []

    return [obj["_source"] for obj in scan(
        get_client(),
        query=dict(
            query=dict(terms={"_id": doc_ids}),
            _source=source_fields),
        size=len(doc_ids),
        index=index)]


def make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True):
    # test_docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # elasticsearch.make_nlp_docs_from_docs_metadata(test_docs_metadata.find({}))
    existing_ids = set()

    if ignore_existing:
        existing_ids = get_ids(index=DOC_INDEX)

        # for obj in scan(get_client(), query=dict(
        #         query=dict(match_all={}),
        #         fields=["_id"]),
        #         size=5000,
        #         index=DOC_INDEX):
        #     existing_ids.add(obj["_id"])

    root_path = Path(get_path_from_root())

    for ix, data in enumerate(docs_metadata):
        doc_path = root_path / data["path_original"]
        if ix and ix % 10000 == 0:
            print(ix)

        if data["_id"] in existing_ids:
            continue

        if not doc_path.exists():
            continue

        # create and save and article
        nlp_doc = NLPDoc(meta={'id': data["_id"]}, **data)

        with open(doc_path, 'rb') as open_file:
            doc = open_file.read().decode('utf-8', errors='ignore')
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

    for (year, count, selected) in response.facets.publishing_frequency:
        print(year.strftime('%Y'), ' (SELECTED):' if selected else ':', count)


def text_search(query, from_result=0, size=10, return_body=False, ignore_cache=False):
    query = MultiMatch(query=query, fields=["title", "body"])

    search = Search(using=get_client(), index=DOC_INDEX)
    search = search.query(query)

    search = search[from_result: from_result + size]

    if not return_body:
        search = search.source(excludes=["body", "doc"])

    response = search.execute(ignore_cache=ignore_cache)

    return response


def ids_search(ids, from_result=0, size=10, return_body=False, ignore_cache=False):
    search = Search(using=get_client(), index=DOC_INDEX)
    search = search.filter("ids", values=ids)

    search = search[from_result: from_result + size]

    if not return_body:
        search = search.source(excludes=["body", "doc"])

    response = search.execute(ignore_cache=ignore_cache)

    return response


# for dobj in scan(es, query={"query": {"match_all": {}}, "fields": []}, size=10000, index="nlp-documents", doc_type=elasticsearch.NLPDoc):

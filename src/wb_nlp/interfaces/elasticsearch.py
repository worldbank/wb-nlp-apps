from datetime import datetime

from pathlib import Path

# from elasticsearch import helpers
from elasticsearch import Elasticsearch

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from elasticsearch_dsl.query import MultiMatch, Match

from wb_nlp.dir_manager import get_path_from_root

connections.create_connection(hosts=['es01'])


_ES_CLIENT = None


def get_client():
    global _ES_CLIENT
    if _ES_CLIENT is None:
        _ES_CLIENT = Elasticsearch(hosts=[{"host": "es01", "port": 9200}])

    return _ES_CLIENT


class NLPDoc(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    author = Keyword()
    country = Keyword()
    corpus = Keyword()
    date_published = Date()
    last_update_date = Date()
    year = Integer()
    tokens = Integer()
    views = Integer()

    class Index:
        name = 'nlp-documents'
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 1,
        }

    def save(self, **kwargs):
        self.tokens = len(self.body.split())
        self.views = 0
        return super(NLPDoc, self).save(**kwargs)


NLPDoc.init()


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


def make_nlp_docs_from_docs_metadata(docs_metadata):
    # test_docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # elasticsearch.make_nlp_docs_from_docs_metadata(test_docs_metadata.find({}))

    root_path = Path(get_path_from_root())

    for data in docs_metadata:
        doc_path = root_path / data["path_original"]

        # create and save and article
        nlp_doc = NLPDoc(meta={'id': data["_id"]}, **data)

        with open(doc_path, 'rb') as open_file:
            doc = open_file.read().decode('utf-8', errors='ignore')
            nlp_doc.body = doc

        nlp_doc.save()


def faceted_search_nlp_docs():
    ns = NLPDocFacetedSearch()
    response = ns.execute()

    for hit in response:
        print(hit.meta.score, hit.title)

    for (country, count, selected) in response.facets.countries:
        print(country, ' (SELECTED):' if selected else ':', count)

    for (year, count, selected) in response.facets.publishing_frequency:
        print(year.strftime('%Y'), ' (SELECTED):' if selected else ':', count)


def text_search(query, from_result=0, to_result=10, return_body=False, ignore_cache=False):
    query = MultiMatch(query=query, fields=["title", "body"])

    search = Search(using=get_client(), index="nlp-documents")
    search = search.query(query)

    search = search[from_result:to_result]

    if not return_body:
        search = search.source(excludes=["body", "doc"])

    response = search.execute(ignore_cache=ignore_cache)

    return response

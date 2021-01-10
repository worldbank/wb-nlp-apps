from datetime import datetime
from pathlib import Path
import hashlib

from elasticsearch import helpers
from elasticsearch import Elasticsearch
from wb_nlp.dir_manager import get_data_dir


# curl -X GET "localhost:9200/_cat/nodes?v&pretty"
# curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'
# curl -XPUT "http://localhost:9200/_cluster/settings" \
#  -H 'Content-Type: application/json' -d'
# {
#   "persistent": {
#     "cluster": {
#       "routing": {
#         "allocation.disk.threshold_enabled": false
#       }
#     }
#   }
# }'

es = Elasticsearch(hosts=[{"host": "es01", "port": 9200}])  # ,
#    request_timeout=60, timeout=60, max_retries=1, retry_on_timeout=True)

INDEX_NAME = 'raw-documents'
INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    }
}


def gen_doc_data(index, doc_path, corpus):
    '''Load text data in `doc_path` into the `index`.
    Reference: https://elasticsearch-py.readthedocs.io/en/master/helpers.html
    '''
    for ix, p in enumerate(Path(doc_path).glob('*.txt'), 1):
        kb_fsize = p.stat().st_size / 1000
        print(ix, p, kb_fsize)
        with open(p, 'rb') as open_file:
            hex_id = hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15]
            doc = open_file.read().decode('utf-8', errors='ignore')
            yield dict(
                _index=index,
                _id=hex_id,
                _source=dict(
                    doc=doc,
                    ix=ix,
                    doc_fname=str(p),
                    doc_id=hex_id,
                    file_size=kb_fsize,
                    timestamp=datetime.now(),
                    corpus=corpus,
                ),
                _op_type="index",
            )


# if es.indices.exists(index=INDEX_NAME):
#     es.indices.delete(index=INDEX_NAME)


if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)
else:
    es.indices.delete(index=INDEX_NAME)
    es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)

p_bulk = helpers.parallel_bulk(
    es, actions=gen_doc_data(
        INDEX_NAME,
        get_data_dir(
            'raw', 'sample_data', 'TXT_ORIG'),
        corpus='WB'
    ),
    thread_count=4, chunk_size=10)

for success, info in p_bulk:
    if not success:
        print('A document failed:', info)

es.indices.refresh(INDEX_NAME)
print(es.cat.count(INDEX_NAME, params={"format": "json"}))

# doc_path = get_data_dir('raw', 'sample_data', 'TXT_ORIG')
# corpus = "WB"

# for ix, p in enumerate(Path(doc_path).glob('*.txt'), 1):
#     kb_fsize = p.stat().st_size / 1000
#     print(ix, p, kb_fsize)
#     with open(p, 'rb') as open_file:
#         hex_id = hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15]
#         int_id = int(hex_id, 16)
#         doc = open_file.read().decode('utf-8', errors='ignore')
#         body = dict(
#             # doc=doc,
#             ix=ix,
#             doc_fname=str(p),
#             doc_id=hex_id,
#             file_size=kb_fsize,
#             # timestamp=datetime.now(),
#             corpus=corpus,
#         )

#         res = es.index(INDEX_NAME, body=body, id=hex_id)


# res = es.get(index="test-index", id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


# es = Elasticsearch()
# es = Elasticsearch(hosts=[{"host": "es01", "port": 9200}])

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", id=1, body=doc)
# print(res['result'])


# {'raw-documents': {'aliases': {},
#   'mappings': {},
#   'settings': {'index': {'routing': {'allocation': {'include': {'_tier_preference': 'data_content'}}},
#     'number_of_shards': '1',
#     'provided_name': 'raw-documents',
#     'creation_date': '1610255433359',
#     'number_of_replicas': '1',
#     'uuid': 'bBIL78PVRZWFQXrJKnWwxQ',
#     'version': {'created': '7100199'}}}},
#  'test-index': {'aliases': {},
#   'mappings': {'properties': {'author': {'type': 'text',
#      'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}},
#     'text': {'type': 'text',
#      'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}}},
#     'timestamp': {'type': 'date'}}},
#   'settings': {'index': {'routing': {'allocation': {'include': {'_tier_preference': 'data_content'}}},
#     'number_of_shards': '1',
#     'provided_name': 'test-index',
#     'creation_date': '1609260406767',
#     'number_of_replicas': '1',
#     'uuid': 'x-_BvHLGSxy9jOgneNyNpA',
#     'version': {'created': '7100199'}}}}}

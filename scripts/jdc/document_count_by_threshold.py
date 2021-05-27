from elasticsearch.helpers import scan
from wb_nlp.interfaces import elasticsearch


def get_ids(doc_index, query=None, ids_only=True):
    # doc_index: NLPDoc, DocTopic, etc.

    index = doc_index.Index.name

    search_query = {}

    if query is None:
        search_query["query"] = dict(match_all={})
    else:
        search_query["query"] = query

    if ids_only:
        search_query["_source"] = ["id"]

    existing_ids = {obj["_source"]["id"] for obj in scan(elasticsearch.get_client(), query=search_query,
                                                         size=5000,
                                                         index=index)}

    return existing_ids


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


def get_unique_tags_query(min_count=2):
    # curl -X GET "es01:9200/_search?pretty" -H 'Content-Type: application/json' -d'{"query": {"bool": {"filter": {"script": {"script": "return doc[\u0027der_jdc_tags\u0027].length >= 2;"}}}}}'

    unique_tags_query = {"query": {"bool": {"filter": {"script": {
        "script": f"return doc['der_jdc_tags'].length >= {min_count};"}}}}}

    # search = elasticsearch.NLPDoc.search()
    # search.from_dict(unique_tags_query).count()

    return unique_tags_query["query"]


topic_model_id = "6fd8b418cbe4af7a1b3d24debfafa1ee"
# Refugee topic for mallet model: 6fd8b418cbe4af7a1b3d24debfafa1ee
topic_percentage = {39: 0.01}

model_run_info_id = topic_model_id

search_topic = elasticsearch.DocTopic.search()


search_topic = search_topic.query(
    get_topic_threshold_query(model_run_info_id, topic_percentage))

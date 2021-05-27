import pandas as pd
from elasticsearch.helpers import scan
from wb_nlp import dir_manager
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


def get_jdc_docs_by_total_word_count():
    search = elasticsearch.NLPDoc.search(index=elasticsearch.NLPDoc.Index.name)

    jdc_total_word_count_script = """
    int total = 0;
    def data = params['_source']['der_jdc_data'];

    for (def i = 0; i < data.length; i++) {
        total += data[i].count
    }

    return total
    """

    search = search.script_fields(jdc_word_count=jdc_total_word_count_script)

    return search


"""
# Pipeline
1. Get the ids based on the topic filter.
2. Get the documents (NLPDoc) of the ids.
3. Use the der_jdc_data.count to test for the frequency condition.
"""


def get_jdc_docs_stats(ids):
    # docs = elasticsearch.NLPDoc.mget(ids)
    index = elasticsearch.NLPDoc.Index.name

    search = elasticsearch.NLPDoc.search()
    search = search.filter("ids", values=list(ids))
    search = search.source(includes=["id", "der_jdc_data"])

    search_query = search.to_dict()

    dataset = []
    for result in scan(elasticsearch.get_client(), query=search_query,
                       size=5000,
                       index=index):

        data = result["_source"]

        dataset.append(
            dict(id=data["id"], total_words=sum(
                [i["count"] for i in data["der_jdc_data"]]), num_tags=len(data["der_jdc_data"]))
        )

    return dataset


def get_topics_by_id(model_run_info_id, topic_ids, ids):
    # doc_index: NLPDoc, DocTopic, etc.

    index = elasticsearch.DocTopic.Index.name

    ids_topic = [f"{model_run_info_id}-{i}" for i in ids]

    search = elasticsearch.DocTopic.search()
    search = search.filter("term", model_run_info_id=model_run_info_id).filter(
        "ids", values=ids_topic)
    search = search.source(
        includes=["id"] + [f"topics.topic_{i}" for i in topic_ids])

    search_query = search.to_dict()

    dataset = []
    for result in scan(elasticsearch.get_client(), query=search_query,
                       size=5000,
                       index=index):

        data = result["_source"]

        data.update(data.pop("topics"))
        dataset.append(data)

    return dataset


def get_topic_jdc_stats(model_run_info_id, topic_percentage):

    topic_ids = list(topic_percentage)

    print("Getting ids_by_topic")
    ids_by_topic = get_ids(elasticsearch.DocTopic, query=get_topic_threshold_query(
        model_run_info_id, topic_percentage), ids_only=True)

    print("Getting ids_by_topic_with_tags")
    ids_by_topic_with_tags = get_ids(
        elasticsearch.NLPDoc,
        query=elasticsearch.NLPDoc.search().filter(
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


# Refugee topic for mallet model: 6fd8b418cbe4af7a1b3d24debfafa1ee
topic_model_id = "6fd8b418cbe4af7a1b3d24debfafa1ee"
topic_percentage = {39: 0.01}

# search_topic = elasticsearch.DocTopic.search()
# search_topic = search_topic.query(
#     get_topic_threshold_query(topic_model_id, topic_percentage))


data = get_topic_jdc_stats(topic_model_id, topic_percentage)

data.to_csv(dir_manager.get_data_dir("jdc_docs_stats.csv"), index=None)

# curl - X GET "es01:9200/nlp-documents/_mapping?pretty"

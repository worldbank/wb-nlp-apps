from wb_nlp import dir_manager
from wb_nlp.interfaces import elasticsearch


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


if __name__ == "__main__":
    # Refugee topic for mallet model: 6fd8b418cbe4af7a1b3d24debfafa1ee
    topic_model_id = "6fd8b418cbe4af7a1b3d24debfafa1ee"
    topic_percentage = {39: 0.01}

    # search_topic = elasticsearch.DocTopic.search()
    # search_topic = search_topic.query(
    #     get_topic_threshold_query(topic_model_id, topic_percentage))

    data = elasticsearch.get_topic_jdc_stats(topic_model_id, topic_percentage)

    data.to_csv(dir_manager.get_data_dir("jdc_docs_stats.csv"), index=None)

    # curl - X GET "es01:9200/nlp-documents/_mapping?pretty"

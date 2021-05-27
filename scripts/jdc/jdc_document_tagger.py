from wb_nlp.interfaces import elasticsearch

# Refugee topic for mallet model: 6fd8b418cbe4af7a1b3d24debfafa1ee
# TOPIC_MODEL_ID = "4472e70cc0a0c2263622b4cbe3aa4644"
TOPIC_MODEL_ID = "6fd8b418cbe4af7a1b3d24debfafa1ee"
TOPIC_ID = 39
TOPIC_PERCENTAGE = 0.01

TOPIC_THRESHOLD = 0.01
AT_LEAST_NUM_TAGS = 2

topic_percentage = {TOPIC_ID: TOPIC_PERCENTAGE}

data = elasticsearch.get_topic_jdc_stats(TOPIC_MODEL_ID, topic_percentage)

jdc_data = data[(data["num_tags"] >= AT_LEAST_NUM_TAGS) &
                (data[f"topic_{TOPIC_ID}"] >= TOPIC_THRESHOLD)]
jdc_doc_ids = jdc_data["id"].tolist()

elasticsearch.set_app_tag_jds(jdc_doc_ids)

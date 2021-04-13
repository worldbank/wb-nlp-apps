'''This router contains the implementation for the cleaning API.
'''
from fastapi import APIRouter, Query
from wb_nlp.types.models import (
    ModelTypes,
    TopicCompositionParams, PartitionTopicShareParams
)
from . import topic_model

router = APIRouter(
    prefix="/lda",
    tags=["LDA Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

LDA_MODEL_NAME = ModelTypes("lda")


DEFAULT_QUERY_FIELDS = topic_model.DEFAULT_QUERY_FIELDS

# dict(
#     model_id=Query(..., description="Model id"),
#     topn_words=Query(
#         10, description="The number of top words that will be returned for each topic."),
#     total_word_score=Query(
#         None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)"),
#     topic_id=Query(..., description="Topic id of interest."),
#     text=Query(..., description="Input text for topic inference."),
#     topn_topics=Query(
#         10, description="The number of topics that will be returned."),
#     total_topic_score=Query(
#         None, description="This will return the topics representing the text with at least `total_topic_score` of cumulative score (order from largest value.)"),
# )


@ router.get("/get_model_topic_words")
async def get_model_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):
    return topic_model.get_model_topic_words(
        model_name=LDA_MODEL_NAME,
        model_id=model_id,
        topn_words=topn_words,
        total_word_score=total_word_score
    )


@ router.get("/get_model_topic_ranges")
async def get_model_topic_ranges(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
):
    return topic_model.get_model_topic_ranges(
        model_name=LDA_MODEL_NAME,
        model_id=model_id
    )


@ router.get("/get_topic_words")
async def get_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    topic_id: int = DEFAULT_QUERY_FIELDS["topic_id"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):
    return topic_model.get_topic_words(
        model_name=LDA_MODEL_NAME,
        model_id=model_id,
        topic_id=topic_id,
        topn_words=topn_words,
        total_word_score=total_word_score
    )


@ router.get("/get_doc_topic_words")
async def get_doc_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    text: str = Query(..., description="Input text for topic inference."),
    topn_topics: int = DEFAULT_QUERY_FIELDS["topn_topics"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_topic_score: float = DEFAULT_QUERY_FIELDS["total_topic_score"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):
    return topic_model.get_doc_topic_words(
        model_name=LDA_MODEL_NAME,
        model_id=model_id,
        text=text,
        topn_topics=topn_topics,
        topn_words=topn_words,
        total_topic_score=total_topic_score,
        total_word_score=total_word_score
    )


@ router.post("/get_docs_by_topic_composition")
async def get_docs_by_topic_composition(
    transform_params: TopicCompositionParams
):
    return topic_model.get_docs_by_topic_composition(
        model_name=LDA_MODEL_NAME,
        transform_params=transform_params
    )


@ router.post("/get_docs_by_topic_composition_count")
async def get_docs_by_topic_composition_count(
    transform_params: TopicCompositionParams
):

    return topic_model.get_docs_by_topic_composition_count(
        model_name=LDA_MODEL_NAME,
        transform_params=transform_params
    )


@ router.post("/get_partition_topic_share")
async def get_partition_topic_share(
    transform_params: PartitionTopicShareParams
):
    return topic_model.get_partition_topic_share(
        model_name=LDA_MODEL_NAME,
        transform_params=transform_params
    )


@ router.get("/get_topics_by_doc_id")
async def get_topics_by_doc_id(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    doc_id: str = Query(..., description="Document id"),
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"],
    sort: bool = Query(
        True, description="Sort the result from largest topic value."),
    format_words: bool = Query(
        True, description="Flag whether the returned topic words will be in a string formatted value.")
):

    return topic_model.get_topics_by_doc_id(
        model_name=LDA_MODEL_NAME,
        model_id=model_id,
        doc_id=doc_id,
        topn_words=topn_words,
        total_word_score=total_word_score,
        sort=sort,
        format_words=format_words
    )

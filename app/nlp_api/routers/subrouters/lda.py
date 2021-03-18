'''This router contains the implementation for the cleaning API.
'''
import enum
import json
from typing import Optional, List
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel, Field

from ...common.utils import get_validated_model
from wb_nlp.dir_manager import get_path_from_root
from wb_nlp.types.models import (
    LDATransformParams, ModelTypes,
    TopicCompositionParams, PartitionTopicShareParams
)
from wb_nlp.interfaces import mongodb


router = APIRouter(
    prefix="/lda",
    tags=["LDA Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

LDA_MODEL_NAME = ModelTypes("lda")


DEFAULT_QUERY_FIELDS = dict(
    model_id=Query(..., description="Model id"),
    topn_words=Query(
        10, description="The number of top words that will be returned for each topic."),
    total_word_score=Query(
        None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)"),
    topic_id=Query(..., description="Topic id of interest."),
    text=Query(..., description="Input text for topic inference."),
    topn_topics=Query(
        10, description="The number of topics that will be returned."),
    total_topic_score=Query(
        None, description="This will return the topics representing the text with at least `total_topic_score` of cumulative score (order from largest value.)"),
)


@ router.post("/get_text_topics")
async def get_topics(model_type: str = None):
    '''This endpoint returns the configurations used to train the available models of the given `model_type`.

    This can be used in the frontend to generate guidance and information about the available models.
    '''

    return dict(model_type=model_type)


@ router.get("/get_model_topic_words")
async def get_model_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):
    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_model_topic_words(
        topn_words=topn_words,
        total_word_score=total_word_score)


@ router.get("/get_model_topic_ranges")
async def get_model_topic_ranges(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
):
    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_topic_composition_ranges()


@ router.get("/get_topic_words")
async def get_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    topic_id: int = DEFAULT_QUERY_FIELDS["topic_id"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):

    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_topic_words(
        topic_id=topic_id,
        topn_words=topn_words,
        total_word_score=total_word_score)


@ router.get("/get_doc_topic_words")
async def get_doc_topic_words(
    model_id: str = DEFAULT_QUERY_FIELDS["model_id"],
    text: str = Query(..., description="Input text for topic inference."),
    topn_topics: int = DEFAULT_QUERY_FIELDS["topn_topics"],
    topn_words: int = DEFAULT_QUERY_FIELDS["topn_words"],
    total_topic_score: float = DEFAULT_QUERY_FIELDS["total_topic_score"],
    total_word_score: float = DEFAULT_QUERY_FIELDS["total_word_score"]
):

    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_doc_topic_words(
        text=text,
        topn_topics=topn_topics,
        topn_words=topn_words,
        total_topic_score=total_topic_score,
        total_word_score=total_word_score)


@ router.post("/get_docs_by_topic_composition")
async def get_docs_by_topic_composition(
    transform_params: TopicCompositionParams
):
    model = get_validated_model(LDA_MODEL_NAME, transform_params.model_id)

    topic_percentage = {
        int(k.split("_")[1]): v for k, v in transform_params.topic_percentage.items()}

    from_result = transform_params.from_result
    size = transform_params.size
    result = model.get_docs_by_topic_composition(
        topic_percentage=topic_percentage,
        from_result=from_result,
        size=size,
        return_all_topics=transform_params.return_all_topics)

    id_rank = {res["id"]: res["rank"] for res in result["hits"]}

    docs_metadata = mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = mongodb.get_docs_metadata_collection()

    response = docs_metadata.find({"id": {"$in": list(id_rank.keys())}})

    total = dict(
        value=result["total"],
        message="many"
    )

    return dict(
        total=total,
        hits=[h for h in sorted(response, key=lambda x: id_rank[x["id"]])],
        api_result=result,
        next=from_result + size,
        result=result,
    )


@ router.post("/get_docs_by_topic_composition_count")
async def get_docs_by_topic_composition_count(
    transform_params: TopicCompositionParams
):
    model = get_validated_model(LDA_MODEL_NAME, transform_params.model_id)

    topic_percentage = {
        int(k.split("_")[1]): v for k, v in transform_params.topic_percentage.items()}

    return dict(total=model.get_docs_by_topic_composition_count(topic_percentage=topic_percentage))


@ router.post("/get_partition_topic_share")
async def get_partition_topic_share(
    transform_params: PartitionTopicShareParams
):
    model = get_validated_model(LDA_MODEL_NAME, transform_params.model_id)

    transform_params = json.loads(transform_params.json())
    transform_params.pop("model_id")

    return model.get_partition_topic_share(**transform_params)

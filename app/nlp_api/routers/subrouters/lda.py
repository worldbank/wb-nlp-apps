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
from wb_nlp.types.models import LDATransformParams, ModelTypes


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
    model_id: str = Query(..., description="Model id"),
    topn_words: int = Query(
        10, description="The number of top words that will be returned for each topic."),
    total_word_score: float = Query(
        None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)")
):
    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_model_topic_words(
        topn_words=topn_words,
        total_word_score=total_word_score)


@ router.get("/get_topic_words")
async def get_topic_words(
    model_id: str = Query(..., description="Model id"),
    topic_id: int = Query(..., description="Topic id of interest."),
    topn_words: int = Query(
        10, description="The number of top words that will be returned for each topic."),
    total_word_score: float = Query(
        None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)")
):

    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_topic_words(
        topic_id=topic_id,
        topn_words=topn_words,
        total_word_score=total_word_score)


@ router.get("/get_doc_topic_words")
async def get_doc_topic_words(
    model_id: str = Query(..., description="Model id"),
    text: str = Query(..., description="Input text for topic inference."),
    topn_topics: int = Query(
        10, description="The number of topics that will be returned."),
    topn_words: int = Query(
        10, description="The number of top words that will be returned for each topic."),
    total_topic_score: float = Query(
        None, description="This will return the topics representing the text with at least `total_topic_score` of cumulative score (order from largest value.)"),
    total_word_score: float = Query(
        None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)")
):

    model = get_validated_model(LDA_MODEL_NAME, model_id)

    return model.get_doc_topic_words(
        text=text,
        topn_topics=topn_topics,
        topn_words=topn_words,
        total_topic_score=total_topic_score,
        total_word_score=total_word_score)

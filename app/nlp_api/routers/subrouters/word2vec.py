'''This router contains the implementation for the cleaning API.
'''

from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from pydantic import BaseModel, Field


from wb_nlp.types.models import (
    ModelTypes, SimilarWordsGraphParams
)

from ...common.utils import get_validated_model

router = APIRouter(
    prefix="/word2vec2",
    tags=["Word2vec Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.post("/get_similar_words_graph")
async def get_similar_words(transform_params: SimilarWordsGraphParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''
    model = get_validated_model(ModelTypes(
        "word2vec"), transform_params.model_id)

    return model.get_similar_words_graph(
        document=transform_params.raw_text,
        topn=transform_params.topn_words,
        edge_thresh=transform_params.edge_thresh,
        n_clusters=transform_params.n_clusters,
        metric=transform_params.metric.value)

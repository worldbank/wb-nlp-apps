'''This router contains the implementation for the cleaning API.
'''
import enum
import json
from typing import Optional, List
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from pydantic import BaseModel, Field

from wb_nlp.interfaces import mongodb

from wb_nlp.dir_manager import get_path_from_root
from wb_nlp.types.models import (
    ModelTypes, Word2VecGetVectorParams,
)
from wb_nlp.models import word2vec_base, lda_base


router = APIRouter(
    prefix="/word2vec",
    tags=["Word2vec Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@lru_cache(maxsize=32)
def get_model_by_model_id(model_id):
    model_runs_info_collection = mongodb.get_model_runs_info_collection()
    model_run_info = model_runs_info_collection.find_one({"_id": model_id})

    if model_run_info["model_name"] == ModelTypes.word2vec.value:

        model = word2vec_base.Word2VecModel(
            model_config_id=model_run_info["model_config_id"],
            cleaning_config_id=model_run_info["cleaning_config_id"],
            raise_empty_doc_status=False,
        )

    elif model_run_info["model_name"] == ModelTypes.lda.value:

        model = lda_base.LDAModel(
            model_config_id=model_run_info["model_config_id"],
            cleaning_config_id=model_run_info["cleaning_config_id"],
            raise_empty_doc_status=False,
        )

    return model


@ router.post("/get_text_vector")
async def get_text_vector(transform_params: Word2VecGetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model_id = transform_params.model_id
    raw_text = transform_params.raw_text
    normalize = transform_params.normalize

    assert transform_params.model_type == ModelTypes.word2vec

    model = get_model_by_model_id(model_id)

    return model.transform_doc(raw_text, normalize=normalize)


@ router.post("/get_file_vector")
async def get_file_vector(file: UploadFile = File(None, description='File to upload.')):
    '''This endpoint converts the `file` provided into a vector transformed using the specified word2vec model.
    '''

    # Word2VecTransformParams

    return dict(file=file)


@ router.post("/get_related_words")
async def get_related_words(transform_params: Word2VecGetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model_id = transform_params.model_id
    raw_text = transform_params.raw_text
    assert transform_params.model_type == ModelTypes.word2vec

    print(model_id, raw_text)

    return dict(transform_params=transform_params)


@ router.post("/get_similar_docs_by_id")
async def get_similar_docs_by_id(transform_params: Word2VecGetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model_id = transform_params.model_id
    raw_text = transform_params.raw_text
    assert transform_params.model_type == ModelTypes.word2vec

    print(model_id, raw_text)

    return dict(transform_params=transform_params)


@ router.post("/get_similar_docs")
async def get_similar_docs(transform_params: Word2VecGetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model_id = transform_params.model_id
    raw_text = transform_params.raw_text
    assert transform_params.model_type == ModelTypes.word2vec

    print(model_id, raw_text)

    return dict(transform_params=transform_params)

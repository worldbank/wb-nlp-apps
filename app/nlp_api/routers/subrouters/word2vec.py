'''This router contains the implementation for the cleaning API.
'''
import enum
import json
from typing import Optional, List
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from pydantic import BaseModel, Field


from wb_nlp.dir_manager import get_path_from_root
from wb_nlp.types.models import (
    ModelTypes, Word2VecGetVectorParams,
)


router = APIRouter(
    prefix="/word2vec",
    tags=["Word2vec Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.post("/get_text_vector")
async def get_text_vector(transform_params: Word2VecGetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model_id = transform_params.model_id
    raw_text = transform_params.raw_text
    assert transform_params.model_type == ModelTypes.word2vec

    print(model_id, raw_text)

    return dict(transform_params=transform_params)


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

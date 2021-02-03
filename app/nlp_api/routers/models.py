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
    ModelTypes, GetVectorParams, SimilarWordsParams, SimilarDocsParams,
    SimilarWordsByDocIDParams, SimilarDocsByDocIDParams
)

from ..common.utils import get_model_by_model_id, process_config


router = APIRouter(
    prefix="/models",
    tags=["Models"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def get_validated_model(model_name, model_id):
    model_run_info = get_model_by_model_id(model_id)

    if model_name != ModelTypes(model_run_info["model_name"]):
        run_model_name = model_run_info["model_name"]
        raise HTTPException(
            status_code=404, detail=f"Invalid model_id: {model_id} for {model_name.value}. This model_id corresponds to a {run_model_name} model.")

    return model_run_info["model"]

# @lru_cache(maxsize=64)
# def process_config(path: Path):
#     if not path.exists():
#         return None

#     model_id = path.parent.name

#     with open(path) as json_file:
#         config = json.load(json_file)
#     config.pop('paths')
#     config['meta']['model_id'] = model_id

#     return config


@ router.get("/get_model_configs")
async def get_model_configs(model_type: ModelTypes):
    '''This endpoint returns the configurations used to train the available models of the given `model_type`.

    This can be used in the frontend to generate guidance and information about the available models.
    '''

    model_path = Path(get_path_from_root('models', model_type.value))
    config_paths = model_path.glob('*/model_config_*.json')
    print(config_paths)

    configs = map(process_config, config_paths)

    model_configs = list(filter(lambda x: x, configs))

    return dict(model_configs=model_configs)


def infer(model_type: ModelTypes, model_id: str):
    pass


@ router.post("/{model_name}/get_text_vector")
async def get_text_vector(model_name: ModelTypes, transform_params: GetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    return model.transform_doc(
        document=transform_params.raw_text,
        normalize=transform_params.normalize,
        tolist=True)


@ router.post("/{model_name}/get_file_vector")
async def get_file_vector(model_name: ModelTypes, file: UploadFile = File(None, description='File to upload.')):
    '''This endpoint converts the `file` provided into a vector transformed using the specified word2vec model.
    '''

    # Word2VecTransformParams

    return dict(file=file)


@ router.post("/{model_name}/get_similar_words")
async def get_similar_words(model_name: ModelTypes, transform_params: SimilarWordsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''
    model = get_validated_model(model_name, transform_params.model_id)

    return model.get_similar_words(
        document=transform_params.raw_text,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/{model_name}/get_similar_docs")
async def get_similar_docs(model_name: ModelTypes, transform_params: SimilarDocsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    result = model.get_similar_documents(
        document=transform_params.raw_text,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type)

    return result


@ router.post("/{model_name}/get_similar_words_by_doc_id")
async def get_similar_words_by_doc_id(model_name: ModelTypes, transform_params: SimilarWordsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    return model.get_similar_words_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/{model_name}/get_similar_docs_by_doc_id")
async def get_similar_docs_by_doc_id(model_name: ModelTypes, transform_params: SimilarDocsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    result = model.get_similar_docs_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type)

    return result

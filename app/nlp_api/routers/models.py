'''This router contains the implementation for the cleaning API.
'''
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
import pydantic

from wb_nlp.interfaces import mongodb

from wb_nlp.types.models import (
    ModelTypes, GetVectorParams, SimilarWordsParams, SimilarDocsParams,
    SimilarWordsByDocIDParams, SimilarDocsByDocIDParams, ModelRunInfo, GetVectorReturns, SimilarWordsReturns,
    SimilarWordsByDocIDReturns,
    SimilarDocsReturns,
    SimilarDocsByDocIDReturns
)

from ..common.utils import get_validated_model


router = APIRouter(
    prefix="/models",
    tags=["Models"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_available_models")
async def get_available_models(
    model_type: ModelTypes,
    expand: bool = Query(
        False,
        description="Flag that indicates whether the returned data will only have the ids for the model and cleaning configs or contain the full information."
    )
):
    '''This endpoint returns a list of all the available models. The returned data contains information regarding the configurations used to train a given model.

    This can be used in the frontend to generate guidance and information about the available models.
    '''
    configs = []

    for conf in mongodb.get_model_runs_info_collection().find({"model_name": model_type.value}):
        try:
            info = json.loads(ModelRunInfo(**conf).json())

            if expand:
                info["model_config"] = mongodb.get_model_configs_collection().find_one(
                    {"_id": info["model_config_id"]})
                info["cleaning_config"] = mongodb.get_cleaning_configs_collection().find_one(
                    {"_id": info["cleaning_config_id"]})

            configs.append(info)

        except pydantic.error_wrappers.ValidationError:
            pass

    return configs


@ router.post("/{model_name}/get_text_vector", response_model=GetVectorReturns)
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


@ router.post("/{model_name}/get_similar_words", response_model=SimilarWordsReturns)
async def get_similar_words(model_name: ModelTypes, transform_params: SimilarWordsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''
    model = get_validated_model(model_name, transform_params.model_id)

    return model.get_similar_words(
        document=transform_params.raw_text,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/{model_name}/get_similar_docs", response_model=SimilarDocsReturns)
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


@ router.post("/{model_name}/get_similar_words_by_doc_id", response_model=SimilarWordsByDocIDReturns)
async def get_similar_words_by_doc_id(model_name: ModelTypes, transform_params: SimilarWordsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    return model.get_similar_words_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/{model_name}/get_similar_docs_by_doc_id", response_model=SimilarDocsByDocIDReturns)
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

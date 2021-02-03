'''This router contains the implementation for the cleaning API.
'''

from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from pydantic import BaseModel, Field


from wb_nlp.types.models import (
    ModelTypes, GetVectorParams, SimilarWordsParams, SimilarDocsParams,
    SimilarWordsByDocIDParams, SimilarDocsByDocIDParams
)

from ...common.utils import get_model_by_model_id

router = APIRouter(
    prefix="/word2vec2",
    tags=["Word2vec Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.post("/get_text_vector")
async def get_text_vector(transform_params: GetVectorParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    assert transform_params.model_type == ModelTypes.word2vec
    model = get_model_by_model_id(transform_params.model_id)

    return model.transform_doc(
        document=transform_params.raw_text,
        normalize=transform_params.normalize,
        tolist=True)


@ router.post("/get_file_vector")
async def get_file_vector(file: UploadFile = File(None, description='File to upload.')):
    '''This endpoint converts the `file` provided into a vector transformed using the specified word2vec model.
    '''

    # Word2VecTransformParams

    return dict(file=file)


@ router.post("/get_similar_words")
async def get_similar_words(transform_params: SimilarWordsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    assert transform_params.model_type == ModelTypes.word2vec
    model = get_model_by_model_id(transform_params.model_id)

    return model.get_similar_words(
        document=transform_params.raw_text,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/get_similar_docs")
async def get_similar_docs(transform_params: SimilarDocsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    assert transform_params.model_type == ModelTypes.word2vec
    model = get_model_by_model_id(transform_params.model_id)

    result = model.get_similar_documents(
        document=transform_params.raw_text,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type)

    return result


@ router.post("/get_similar_words_by_doc_id")
async def get_similar_words_by_doc_id(transform_params: SimilarWordsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    assert transform_params.model_type == ModelTypes.word2vec
    model = get_model_by_model_id(transform_params.model_id)

    return model.get_similar_words_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


@ router.post("/get_similar_docs_by_doc_id")
async def get_similar_docs_by_doc_id(transform_params: SimilarDocsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    assert transform_params.model_type == ModelTypes.word2vec
    model = get_model_by_model_id(transform_params.model_id)

    result = model.get_similar_docs_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type)

    return result

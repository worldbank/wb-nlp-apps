'''This router contains the implementation for the cleaning API.
'''
import json
from fastapi import APIRouter, UploadFile, File, Query  # , HTTPException, Form
import pydantic
from typing import List

from wb_nlp.interfaces import mongodb

from wb_nlp.types.models import (
    ModelTypes, GetVectorParams, SimilarWordsParams, SimilarDocsParams,
    SimilarWordsByDocIDParams, SimilarDocsByDocIDParams, ModelRunInfo, GetVectorReturns, SimilarWordsReturns,
    SimilarWordsByDocIDReturns,
    SimilarDocsReturns,
    SimilarDocsByDocIDReturns,
    # UploadTypes, MetricTypes, MilvusMetricTypes,
)

# , read_uploaded_file, read_url_file
from ..common.utils import get_validated_model, check_translate_keywords


router = APIRouter(
    prefix="/models",
    tags=["Models"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_available_models")
async def get_available_models(
    model_type: List[ModelTypes] = Query(...,
                                         description="List of model names."),
    expand: bool = Query(
        False,
        description="Flag that indicates whether the returned data will only have the ids for the model and cleaning configs or contain the full information."
    )
):
    '''This endpoint returns a list of all the available models. The returned data contains information regarding the configurations used to train a given model.

    This can be used in the frontend to generate guidance and information about the available models.
    '''
    configs = []

    for mt in model_type:
        for conf in mongodb.get_model_runs_info_collection().find({"model_name": mt.value}):
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
    payload = check_translate_keywords(transform_params.raw_text)
    text = payload["query"]

    return model.transform_doc(
        document=text,
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
    payload = check_translate_keywords(transform_params.raw_text)
    text = payload["query"]

    return model.get_similar_words(
        document=text,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


# @ router.post("/{model_name}/get_similar_docs", response_model=SimilarDocsReturns)
@ router.post("/{model_name}/get_similar_docs")
async def get_similar_docs(model_name: ModelTypes, transform_params: SimilarDocsParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)
    payload = check_translate_keywords(transform_params.raw_text)
    text = payload["query"]

    result = model.get_similar_documents(
        document=text,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type.value)

    return result


# @ router.post("/{model_name}/upload/get_similar_docs", response_model=SimilarDocsReturns)
# async def get_upload_similar_docs(


#     model_name: ModelTypes,
#     upload_type: UploadTypes,
#     model_id: str = Form(...),
#     url: str = Form(None),
#     file: UploadFile = File(None),
#     topn_docs: int = Form(
#         10, ge=1, description='Number of similar words to return.'),
#     show_duplicates: bool = Form(
#         False, description='Flag that indicates whether to return highly similar or possibly duplicate documents.'
#     ),
#     duplicate_threshold: float = Form(
#         0.98, ge=0, description='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
#     ),
#         metric_type: MilvusMetricTypes = MilvusMetricTypes.IP):
#     '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
#     '''

#     model = get_validated_model(model_name, model_id)

#     if upload_type == UploadTypes("file_upload"):
#         document = read_uploaded_file(file)
#     elif upload_type == UploadTypes("url_upload"):
#         document = read_url_file(url)

#     document = model.clean_text(document)

#     result = model.get_similar_documents(
#         document=document,
#         topn=topn_docs,
#         duplicate_threshold=duplicate_threshold,
#         show_duplicates=show_duplicates,
#         metric_type=metric_type.value)

#     return result


@ router.post("/{model_name}/get_similar_words_by_doc_id", response_model=SimilarWordsByDocIDReturns)
async def get_similar_words_by_doc_id(model_name: ModelTypes, transform_params: SimilarWordsByDocIDParams):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    return model.get_similar_words_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_words,
        metric=transform_params.metric.value)


# @ router.post("/{model_name}/get_similar_docs_by_doc_id", response_model=SimilarDocsByDocIDReturns)
@ router.post("/{model_name}/get_similar_docs_by_doc_id")
async def get_similar_docs_by_doc_id(model_name: ModelTypes, transform_params: SimilarDocsByDocIDParams, return_metadata: bool = True):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    model = get_validated_model(model_name, transform_params.model_id)

    result = model.get_similar_docs_by_doc_id(
        doc_id=transform_params.doc_id,
        topn=transform_params.topn_docs,
        duplicate_threshold=transform_params.duplicate_threshold,
        show_duplicates=transform_params.show_duplicates,
        metric_type=transform_params.metric_type.value)

    if return_metadata:
        # docs_metadata = mongodb.get_docs_metadata_collection()
        docs_metadata = mongodb.get_collection(
            db_name="test_nlp", collection_name="docs_metadata")
        metadata_map = {d["id"]: d for d in docs_metadata.find(
            {"id": {"$in": [r["id"] for r in result]}})}

        for r in result:
            r["metadata"] = metadata_map[r["id"]]

    return result

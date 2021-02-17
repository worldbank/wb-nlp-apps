'''This router contains the implementation for the cleaning API.
'''
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
import pydantic

from wb_nlp.interfaces import mongodb, elasticsearch

from wb_nlp.types.models import (
    ModelTypes
)
from ..common.utils import get_validated_model


router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/keyword")
async def keyword_search(
    query: str,
    from_result: int = 0,
    size: int = 10,
):
    '''This endpoint returns a list of all the available models. The returned data contains information regarding the configurations used to train a given model.

    This can be used in the frontend to generate guidance and information about the available models.
    '''
    response = elasticsearch.text_search(
        query, from_result=from_result, size=size)

    return dict(
        total=response.hits.total.to_dict(),
        hits=[h.to_dict() for h in response.hits],
        next=from_result + size
    )


@ router.get("/semantic")
async def semantic_search(
    query: str,
    from_result: int = 0,
    size: int = 10,
):
    '''This endpoint returns a list of all the available models. The returned data contains information regarding the configurations used to train a given model.

    This can be used in the frontend to generate guidance and information about the available models.
    '''

    model = get_validated_model(ModelTypes(
        "word2vec"), "777a9cf47411f6c4932e8941f177f90a")

    result = model.search_similar_documents(
        document=query,
        from_result=from_result,
        size=size)

    # Put negative sign since score is expected to be large for relevant items.
    id_rank = {res["id"]: -res["rank"] for res in result}

    # search = elasticsearch.Search(using=elasticsearch.get_client(), index="nlp-documents")
    # search = search.filter("ids", values=)

    # response = search.execute()
    response = elasticsearch.ids_search(
        ids=[i["id"] for i in result],
        from_result=0,
        size=size)

    return dict(
        total=response.hits.total.to_dict(),
        hits=[h.to_dict()
              for h in sorted(response.hits, key=lambda x: id_rank[x["id"]])],
        next=from_result + size
    )

# @ router.post("/{model_name}/get_similar_docs", response_model=SimilarDocsReturns)
# async def get_similar_docs(model_name: ModelTypes, transform_params: SimilarDocsParams):
#     '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
#     '''

#     model = get_validated_model(model_name, transform_params.model_id)

#     result = model.get_similar_documents(
#         document=transform_params.raw_text,
#         topn=transform_params.topn_docs,
#         duplicate_threshold=transform_params.duplicate_threshold,
#         show_duplicates=transform_params.show_duplicates,
#         metric_type=transform_params.metric_type)

#     return result

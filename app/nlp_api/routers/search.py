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

    id_rank = {res["id"]: res["rank"] for res in result}

    response = elasticsearch.ids_search(
        ids=[i["id"] for i in result],
        from_result=0,
        size=size)

    return dict(
        total=response.hits.total.to_dict(),
        hits=[h.to_dict()
              for h in sorted(response.hits, key=lambda x: id_rank[x["id"]])],
        next=from_result + size,
        result=result,
    )
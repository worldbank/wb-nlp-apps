'''This router contains the implementation for the cleaning API.
'''
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
import pydantic

from wb_nlp.interfaces import mongodb, elasticsearch


router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/search")
async def search(
    query: str,
    from_result: int = 0,
    to_result: int = 10,
):
    '''This endpoint returns a list of all the available models. The returned data contains information regarding the configurations used to train a given model.

    This can be used in the frontend to generate guidance and information about the available models.
    '''
    response = elasticsearch.text_search(
        query, from_result=from_result, to_result=to_result)

    return [h.__dict__["_d_"] for h in response.hits]

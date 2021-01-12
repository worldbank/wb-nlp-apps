'''This router contains the implementation for the cleaning API.
'''
import enum
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body


from wb_nlp.types.metadata import MetadataModel

router = APIRouter(
    prefix="/corpus",
    tags=["Corpus"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_metadata", response_model=MetadataModel)
def get_doc_metadata(hex_id: str):

    doc = metadata.MetadataModel(hex_id="1232", int_id=1231, corpus="WB", filename_original="asff.txt", last_update_date=metadata.datetime.now(
    ), path_original="/asdad/wefsdc/asdasd/woiefsdf.txt", title="Hello world", doc_type=['Agreement'])
    return doc

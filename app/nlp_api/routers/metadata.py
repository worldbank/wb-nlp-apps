'''This router contains the implementation for the cleaning API.
'''
import enum
from datetime import datetime
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body

from wb_nlp.interfaces import mongodb
from wb_nlp.types import metadata
# from wb_nlp.types.metadata_enums import Corpus

router = APIRouter(
    prefix="/corpus",
    tags=["Corpus"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_metadata_by_id", response_model=metadata.MetadataModel)
def get_doc_metadata_by_id(id: str):
    """This enpoint fetches the metadata corresponding to the given `id`.
    """

    doc = mongodb.get_docs_metadata_collection().find_one({"id": id})
    doc = metadata.MetadataModel(**doc)

    # doc = MetadataModel(hex_id="1232", int_id=1231, corpus=corpus, filename_original="asff.txt", last_update_date=datetime.now(
    # ), path_original="/asdad/wefsdc/asdasd/woiefsdf.txt", title="Hello world", doc_type=['Agreement'])
    return doc

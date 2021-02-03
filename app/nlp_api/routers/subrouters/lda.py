'''This router contains the implementation for the cleaning API.
'''
import enum
import json
from typing import Optional, List
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, Field


from wb_nlp.dir_manager import get_path_from_root
from wb_nlp.types.models import LDATransformParams


router = APIRouter(
    prefix="/lda2",
    tags=["LDA Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.post("/get_text_topics")
async def get_topics(model_type: str = None):
    '''This endpoint returns the configurations used to train the available models of the given `model_type`.

    This can be used in the frontend to generate guidance and information about the available models.
    '''

    return dict(model_type=model_type)

'''This router contains the implementation for the cleaning API.
'''
from functools import lru_cache
from fastapi import APIRouter, Depends, HTTPException, Body
import pandas as pd
import numpy as np
from pydantic import AnyHttpUrl
import requests
from sklearn.metrics.pairwise import cosine_similarity
from wb_nlp.types.models import (
    ModelTypes, IndicatorTypes
)
from wb_nlp import dir_manager
from wb_nlp.models import wdi_base, sdg_base

from ...common.utils import get_validated_model

router = APIRouter(
    prefix="/indicators",
    tags=["Indicators metadata"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@lru_cache(maxsize=16)
def get_indicator_model(indicator_code, model_id):
    model = get_validated_model(ModelTypes(
        "word2vec"), model_id)

    indicator_model = None

    if indicator_code == IndicatorTypes("wdi"):
        indicator_model = wdi_base.WDIModel(
            wvec_model=model,
            model_config_id=model.model_config_id,
            cleaning_config_id=model.cleaning_config_id,
            model_run_info_id=model.model_id,
        )
    elif indicator_code == IndicatorTypes("sdg"):
        indicator_model = sdg_base.SDGModel(
            wvec_model=model,
            model_config_id=model.model_config_id,
            cleaning_config_id=model.cleaning_config_id,
            model_run_info_id=model.model_id,
        )

    return indicator_model


@lru_cache(maxsize=None)
def _get_wdi_metadata(url_meta):
    response = requests.get(url_meta)
    response = response.json()
    meta = response["source"][0]["concept"][0]["variable"][0]["metatype"]
    return {r["id"]: r["value"] for r in meta}


@ router.get("/{indicator_code}/get_similar_indicators_by_doc_id")
async def get_similar_indicators_by_doc_id(indicator_code: IndicatorTypes, doc_id: str, model_id: str, topn: int = 10):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    indicator_model = get_indicator_model(indicator_code, model_id)

    if indicator_code == IndicatorTypes("wdi"):
        ret_cols = ["id", "name", "score", "url_data", "url_meta", "url_wb"]
    else:
        ret_cols = ["id", "name", "score", "url_data", "url_meta", "goal", "goal_title", "goal_uri", "img_uri",
                    "target", "target_title", "target_uri", "indicator", "indicator_description", "indicator_uri"]

    return indicator_model.get_similar_indicators_by_doc_id(doc_id=doc_id, topn=topn, ret_cols=ret_cols, as_records=True)


@ router.get("/wdi/get_wdi_metadata")
async def get_wdi_metadata(url_meta: AnyHttpUrl):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    data = {"Longdefinition": None, "Shortdefinition": None}
    try:
        data = _get_wdi_metadata(url_meta)
    except Exception as e:
        pass

    return data


# https://api.worldbank.org/v2/sources/2/series/it.net.secr/metadata?format=json

# Longdefinition
# Shortdefinition

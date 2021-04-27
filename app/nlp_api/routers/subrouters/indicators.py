'''This router contains the implementation for the cleaning API.
'''
from functools import lru_cache
from fastapi import APIRouter, UploadFile, File, Form

from pydantic import HttpUrl, AnyHttpUrl

import requests

from wb_nlp.types.models import (
    ModelTypes, IndicatorTypes
)

from wb_nlp.models import wdi_base, sdg_base, microdata_base

from ...common.utils import (
    get_validated_model, read_uploaded_file,
    read_url_file,
)

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
    elif indicator_code == IndicatorTypes("microdata"):
        indicator_model = microdata_base.MicrodataModel(
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


def get_ret_cols(indicator_code: IndicatorTypes):
    if indicator_code == IndicatorTypes("wdi"):
        ret_cols = ["id", "name", "score", "url_data", "url_meta", "url_wb"]
    elif indicator_code == IndicatorTypes("sdg"):
        ret_cols = ["id", "name", "score", "url_data", "url_meta", "goal", "goal_title", "goal_uri", "img_uri",
                    "target", "target_title", "target_uri", "indicator", "indicator_description", "indicator_uri"]
    elif indicator_code == IndicatorTypes("microdata"):
        ret_cols = ["id", "name", "score"]

    return ret_cols


def _get_similar_indicators_by_doc_id(indicator_code: IndicatorTypes, doc_id: str, model_id: str, topn: int = 10):
    indicator_model = get_indicator_model(indicator_code, model_id)
    ret_cols = get_ret_cols(indicator_code)

    return indicator_model.get_similar_indicators_by_doc_id(doc_id=doc_id, topn=topn, ret_cols=ret_cols, as_records=True)


@ router.get("/{indicator_code}/get_similar_indicators_by_doc_id")
async def get_similar_indicators_by_doc_id(indicator_code: IndicatorTypes, doc_id: str, model_id: str, topn: int = 10):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    return _get_similar_indicators_by_doc_id(indicator_code=indicator_code, doc_id=doc_id, model_id=model_id, topn=topn)


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


def get_all_indicators_from_document(model_id: str, document: str, topn: int = 10):
    payload = {}
    doc_vec = None

    for indicator_code in IndicatorTypes:
        indicator_model = get_indicator_model(indicator_code, model_id)
        ret_cols = get_ret_cols(indicator_code)

        if doc_vec is None:
            result = indicator_model.wvec_model.process_doc(
                {"text": document}, normalize=True)
            doc_vec = result["doc_vec"]

        payload[indicator_code.value] = indicator_model.get_similar_indicators_by_vector(
            doc_vec, topn=topn, ret_cols=ret_cols, as_records=True)

    return payload


@ router.post("/all/get_similar_indicators_from_file")
async def get_similar_indicators_from_file(model_id: str = Form(...), file: UploadFile = File(...), topn: int = 10):
    document = read_uploaded_file(file)

    return get_all_indicators_from_document(model_id=model_id, document=document, topn=topn)


@ router.post("/all/get_similar_indicators_from_url")
async def get_similar_indicators_from_url(model_id: str = Form(...), url: HttpUrl = Form(...), topn: int = 10):
    document = read_url_file(url)

    return get_all_indicators_from_document(model_id=model_id, document=document, topn=topn)


# https://api.worldbank.org/v2/sources/2/series/it.net.secr/metadata?format=json

# Longdefinition
# Shortdefinition

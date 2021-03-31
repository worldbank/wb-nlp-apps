'''This router contains the implementation for the cleaning API.
'''

from fastapi import APIRouter, Depends, HTTPException, Body
import pandas as pd
import numpy as np
from pydantic import AnyHttpUrl
import requests
from sklearn.metrics.pairwise import cosine_similarity
from wb_nlp.types.models import (
    ModelTypes
)
from wb_nlp import dir_manager

from ...common.utils import get_validated_model

router = APIRouter(
    prefix="/wdi",
    tags=["WDI metadata"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_similar_wdi_by_doc_id")
async def get_similar_wdi_by_doc_id(doc_id: str, model_id: str, topn: int = 10):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''
    model = get_validated_model(ModelTypes(
        "word2vec"), model_id)

    avec = model.get_milvus_doc_vector_by_doc_id(doc_id).reshape(1, -1)
    wdi_df = pd.read_pickle(dir_manager.get_path_from_root(
        "models", "wdi", f"wdi_time_series_metadata-{model.model_id}.pickle"))

    vecs = np.vstack(wdi_df["vector"].values)
    sim = cosine_similarity(avec, vecs)[0]
    sorted_idx = sim.argsort()[::-1]

    wdi_df["score"] = sim
    wdi_df = wdi_df.iloc[sorted_idx]

    ret_cols = ["id", "name", "url_data", "url_meta", "url_wb", "score"]

    return wdi_df[ret_cols].head(topn).to_dict("records")


@ router.get("/get_wdi_metadata")
async def get_wdi_metadata(url_meta: AnyHttpUrl):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''

    data = {"Longdefinition": None, "Shortdefinition": None}
    try:
        response = requests.get(url_meta)
        response = response.json()
        meta = response["source"][0]["concept"][0]["variable"][0]["metatype"]
        data = {r["id"]: r["value"] for r in meta}
    except:
        pass

    return data

# https://api.worldbank.org/v2/sources/2/series/it.net.secr/metadata?format=json

# Longdefinition
# Shortdefinition

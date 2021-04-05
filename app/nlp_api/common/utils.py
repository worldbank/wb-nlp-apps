from pathlib import Path
import json
from functools import lru_cache
from fastapi import HTTPException
import requests
from wb_nlp.interfaces import mongodb

from wb_nlp.types.models import (
    ModelTypes,
)
from wb_nlp.models import word2vec_base, lda_base
from wb_nlp.processing import document

# This is faster than lru_cache
MODEL_CACHE = {}


@lru_cache(maxsize=64)
def process_config(path: Path):
    if not path.exists():
        return None

    model_id = path.parent.name

    with open(path) as json_file:
        config = json.load(json_file)
    config.pop('paths')
    config['meta']['model_id'] = model_id

    return config


# @lru_cache(maxsize=32)
def get_model_by_model_id(model_id):
    global MODEL_CACHE

    if model_id not in MODEL_CACHE:
        model_runs_info_collection = mongodb.get_model_runs_info_collection()
        model_run_info = model_runs_info_collection.find_one({"_id": model_id})
        print(model_run_info)

        if model_run_info["model_name"] == ModelTypes.word2vec.value:

            model = word2vec_base.Word2VecModel(
                model_config_id=model_run_info["model_config_id"],
                cleaning_config_id=model_run_info["cleaning_config_id"],
                model_run_info_id=model_id,
                raise_empty_doc_status=False,
            )

        elif model_run_info["model_name"] == ModelTypes.lda.value:

            model = lda_base.LDAModel(
                model_config_id=model_run_info["model_config_id"],
                cleaning_config_id=model_run_info["cleaning_config_id"],
                model_run_info_id=model_id,
                raise_empty_doc_status=False,
            )

        model_run_info["model"] = model

        MODEL_CACHE[model_id] = model_run_info

    return MODEL_CACHE[model_id]


def get_validated_model(model_name, model_id):
    model_run_info = get_model_by_model_id(model_id)

    if model_name != ModelTypes(model_run_info["model_name"]):
        run_model_name = model_run_info["model_name"]
        raise HTTPException(
            status_code=404, detail=f"Invalid model_id: {model_id} for {model_name.value}. This model_id corresponds to a {run_model_name} model.")

    return model_run_info["model"]


@lru_cache(maxsize=128)
def read_uploaded_file(file):

    if file.content_type.startswith("text/"):
        text = file.file.read().decode("utf-8", errors="ignore")
    elif file.content_type.startswith("application/pdf"):

        doc = document.PDFDoc2Txt()
        text_pages = doc.parse(source=file.file, source_type="buffer")
        text = " ".join(text_pages)

    return text


@lru_cache(maxsize=128)
def read_url_file(url):

    buf = requests.get(url)

    if buf.headers["Content-Type"].startswith("text/"):
        text = buf.content.decode("utf-8", errors="ignore")
    elif buf.headers["Content-Type"].startswith("application/pdf"):
        doc = document.PDFDoc2Txt()
        text_pages = doc.parse(source=buf.content, source_type="buffer")
        text = " ".join(text_pages)
    else:
        raise HTTPException(
            status_code=404, detail="URL doesn't point to a valid data type. Make sure the url is for a pdf or txt file.")

    return text


@lru_cache(maxsize=128)
def clean_text(model_name, model_id, text):
    model = get_validated_model(model_name, model_id)
    return model.clean_text(text)

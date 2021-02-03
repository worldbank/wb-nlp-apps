from pathlib import Path
import json
from functools import lru_cache
from fastapi import HTTPException

from wb_nlp.interfaces import mongodb

from wb_nlp.types.models import (
    ModelTypes,
)
from wb_nlp.models import word2vec_base, lda_base


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


@lru_cache(maxsize=32)
def get_model_by_model_id(model_id):
    model_runs_info_collection = mongodb.get_model_runs_info_collection()
    model_run_info = model_runs_info_collection.find_one({"_id": model_id})
    print(model_run_info)

    if model_run_info["model_name"] == ModelTypes.word2vec.value:

        model = word2vec_base.Word2VecModel(
            model_config_id=model_run_info["model_config_id"],
            cleaning_config_id=model_run_info["cleaning_config_id"],
            raise_empty_doc_status=False,
        )

    elif model_run_info["model_name"] == ModelTypes.lda.value:

        model = lda_base.LDAModel(
            model_config_id=model_run_info["model_config_id"],
            cleaning_config_id=model_run_info["cleaning_config_id"],
            raise_empty_doc_status=False,
        )

    model_run_info["model"] = model
    return model_run_info


def get_validated_model(model_name, model_id):
    model_run_info = get_model_by_model_id(model_id)

    if model_name != ModelTypes(model_run_info["model_name"]):
        run_model_name = model_run_info["model_name"]
        raise HTTPException(
            status_code=404, detail=f"Invalid model_id: {model_id} for {model_name.value}. This model_id corresponds to a {run_model_name} model.")

    return model_run_info["model"]

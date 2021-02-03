from functools import lru_cache

from wb_nlp.interfaces import mongodb

from wb_nlp.types.models import (
    ModelTypes,
)
from wb_nlp.models import word2vec_base, lda_base


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

    return model

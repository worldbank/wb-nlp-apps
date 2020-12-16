'''This router contains the implementation for the cleaning API.
'''
import enum
import json
from typing import Optional, List
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, Field

import uvicorn

from wb_nlp.cleaning import cleaner
from wb_nlp.dir_manager import get_path_from_root
from wb_nlp.utils.scripts import generate_model_hash


router = APIRouter(
    prefix="/models",
    tags=["Models"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


############# START: DEFINITION OF DATA TYPES AND MODELS #############

class ModelTypes(enum.Enum):
    '''Types of models available.
    '''
    lda = "lda"  # Gensim LDA implementation
    mallet = "mallet"  # Mallet LDA implementation
    word2vec = "word2vec"  # Gensim Word2vec implementation


############# END: DEFINITION OF DATA TYPES AND MODELS #############


class HashableDict(dict):
    '''This is a wrapper class to make a dictionary hashable.
    '''

    def __hash__(self):
        return hash(generate_model_hash(config=self))


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
def get_model_configs(model_type: str):

    model_path = Path(get_path_from_root('models', model_type))
    config_paths = model_path.glob('*/model_config_*.json')

    configs = map(process_config, config_paths)

    return list(filter(lambda x: x, configs))


@ router.get("/get_model_configs")
async def get_model_configs(model_type: str):
    '''This endpoint cleans the given `text` data.

    The cleaning pipeline is setup based on the given configuration parameters.

    Configuration parameters can alter the behavior of the `cleaner`, `respeller`, and `spell checker`.
    '''
    model_configs = get_model_configs(model_type)

    return dict(model_configs=model_configs)

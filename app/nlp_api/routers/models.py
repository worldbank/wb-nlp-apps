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


@ router.get("/get_model_configs")
async def get_model_configs(model_type: ModelTypes):
    '''This endpoint returns the configurations used to train the available models of the given `model_type`.

    This can be used in the frontend to generate guidance and information about the available models.
    '''

    model_path = Path(get_path_from_root('models', model_type.value))
    config_paths = model_path.glob('*/model_config_*.json')
    print(config_paths)

    configs = map(process_config, config_paths)

    model_configs = list(filter(lambda x: x, configs))

    return dict(model_configs=model_configs)

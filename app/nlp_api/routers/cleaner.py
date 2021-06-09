'''This router contains the implementation for the cleaning API.
'''
import enum
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, Field


from wb_cleaning.cleaning import cleaner
from wb_cleaning.types.cleaning import CleaningConfig
from wb_cleaning.utils.data_types import HashableDict

router = APIRouter(
    prefix="/cleaner",
    tags=["Cleaner"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@lru_cache(maxsize=32)
def get_cleaner(config):
    """This creates a cleaner instances and caches (LRU) the
    object based on the config.
    """
    print('Getting cleaner instance...')

    return cleaner.BaseCleaner(config=config)


@ router.post("/clean")
async def clean(
        cleaning_config: CleaningConfig,
        text: str = "Forcibly displaced populations including refugees, internally displaced persons, stateless people, asylum seekers, and host populations.",):
    '''This endpoint cleans the given `text` data.

    The cleaning pipeline is setup based on the given configuration parameters.

    Configuration parameters can alter the behavior of the `cleaner`, `respeller`, and `spell checker`.
    '''
    config = CleaningConfig(**cleaning_config.dict()).dict()
    print(config)

    cleaner_object = get_cleaner(HashableDict(config))
    cleaned_text = cleaner_object.get_clean_tokens(text)

    return dict(
        text=text,
        cleaned_text=cleaned_text,
        cleaning_config=config)

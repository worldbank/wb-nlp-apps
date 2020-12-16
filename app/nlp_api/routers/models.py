'''This router contains the implementation for the cleaning API.
'''
import enum
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, Field

import uvicorn

from wb_nlp.cleaning import cleaner
from wb_nlp.utils.scripts import generate_model_hash


router = APIRouter(
    prefix="/models",
    tags=["Models"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


############# START: DEFINITION OF DATA TYPES AND MODELS #############

class POSTag(enum.Enum):
    '''Enum of SpaCy part-of-speech tags.
    '''
    # SpaCy pos tags
    noun = "NOUN"
    adjective = "ADJ"
    verb = "VERB"
    propn = "PROPN"
    adverb = "ADV"
    # 'ADP', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ',
    # 'NUM', 'PART',


class Entity(enum.Enum):
    '''Enum of SpaCy entities.
    '''
    cardinal = "CARDINAL"
    time = "TIME"
    percent = "PERCENT"
    money = "MONEY"
    date = "DATE"
    quantity = "QUANTITY"
    ordinal = "ORDINAL"


class Params(BaseModel):
    use: bool = True
    params: dict = {}


class RespellerInit(BaseModel):
    dictionary_file: Optional[str] = None
    spell_threshold: float = 0.25
    allow_proper: bool = False  # Don't include proper names in suggestions
    spell_cache: Optional[dict] = None


class RespellerInferCorrectWord(BaseModel):
    sim_thresh: float = 0.0
    print_log: bool = False
    min_len: int = 3
    use_suggest_score: bool = True


class RespellerInferCorrectWords(BaseModel):
    return_tokens_as_list: bool = True


class RespellerConfig(BaseModel):
    init: RespellerInit
    infer_correct_word: RespellerInferCorrectWord
    infer_correct_words: RespellerInferCorrectWords


class SpellCheckerInit(BaseModel):
    lang: str = "en_US"
    text: Optional[str] = None


class SpellCheckerConfig(BaseModel):
    init: SpellCheckerInit
    # tokenize: Optional[str] = None
    # chunkers: Optional[str] = None
    # filters: Optional[str] = None


# class FilterByPOSParams(Params):
#     params:
#     include_pos_tags: List


class CleanerFixFragmentedTokensParams(BaseModel):
    max_len: int = 5


class CleanerFixFragmentedTokens(Params):
    params: CleanerFixFragmentedTokensParams


class CleanerFilterLanguageParams(BaseModel):
    langs: List[str] = ["en"]
    score: float = Field(
        0.98, gt=0, description="Threshold for a detected language to be valid.")


class CleanerFilterLanguage(Params):
    params: CleanerFilterLanguageParams


class CleanerConfig(BaseModel):
    """This defines the data model for the cleaner config.
    """
    # Options for cleaning.corrector.recover_segmented_words
    fix_fragmented_tokens: CleanerFixFragmentedTokens
    # Expand the acronyms in the text
    expand_acronyms: Params
    # Update the spacy doc with the whitelisted entitiy tag
    tag_whitelisted_entities: Params
    # Use the part-of-speech as filter
    filter_by_pos: Params
    # Use extracted entities as filter
    filter_by_entities: Params
    # Check and fix spelling based on the Respeller module
    correct_misspelling: Params
    # Remove stopwords from the text
    filter_stopwords: Params
    # Filter by language
    filter_language: CleanerFilterLanguage
    include_pos_tags: List[POSTag] = [
        POSTag.adjective.value, POSTag.noun.value]
    exclude_entity_types: List[Entity] = [
        Entity.cardinal.value, Entity.time.value]

    class Config:
        schema_extra = {
            "example": "Example"
        }


class POSTagType(BaseModel):
    pos: POSTag


class EntityType(BaseModel):
    ent: Entity

############# END: DEFINITION OF DATA TYPES AND MODELS #############


class HashableDict(dict):
    '''This is a wrapper class to make a dictionary hashable.
    '''

    def __hash__(self):
        return hash(generate_model_hash(config=self))


@lru_cache(maxsize=32)
def get_cleaner(config):
    """This creates a cleaner instances and caches (LRU) the
    object based on the config.
    """
    print('Getting cleaner instance...')

    return cleaner.BaseCleaner(
        config=config,
        include_pos=config['include_pos_tags'],
        exclude_entities=config['exclude_entity_types'],
        min_token_length=config['min_token_length'],
        max_token_length=config['max_token_length']
    )


@ router.post("/clean")
async def clean(
        text: str,
        cleaner_config: CleanerConfig,
        spell_checker_config: SpellCheckerConfig,
        respeller_config: RespellerConfig,
        min_token_length: int = Body(
            3, gt=0, description="Minimum length of token."),
        max_token_length: int = Body(
            50, gt=0, description="Maximum length of token."),

):
    '''This endpoint cleans the given `text` data.

    The cleaning pipeline is setup based on the given configuration parameters.

    Configuration parameters can alter the behavior of the `cleaner`, `respeller`, and `spell checker`.
    '''

    spell_checker_config = spell_checker_config.dict()
    respeller_config = respeller_config.dict()
    cleaner_config = cleaner_config.dict()

    # Cast the data to the acceptable key value as used in the cleaner module.
    spell_checker_config['__init__'] = spell_checker_config.pop('init')
    respeller_config['__init__'] = respeller_config.pop('init')

    config = dict(
        cleaner=cleaner_config,
        spell_checker=spell_checker_config,
        respeller=respeller_config)

    config['min_token_length'] = min_token_length
    config['max_token_length'] = max_token_length

    config['include_pos_tags'] = [
        p.value for p in cleaner_config.pop('include_pos_tags')]
    config['exclude_entity_types'] = [
        e.value for e in cleaner_config.pop('exclude_entity_types')]

    cleaner_object = get_cleaner(HashableDict(config))
    cleaned_text = cleaner_object.get_clean_tokens(text)

    return dict(
        text=text,
        cleaned_text=cleaned_text,
        cleaner_config=config)

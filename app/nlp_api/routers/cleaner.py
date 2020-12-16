'''This router contains the implementation for the cleaning API.
'''
import enum
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import uvicorn

from wb_nlp.cleaning import cleaner

router = APIRouter(
    prefix="/cleaner",
    tags=["cleaner"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


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


# cleaner_config:
#     # https://spacy.io/api/annotation
#     include_pos_tags:
#         # - POS
#         - ADJ
#         # - ADP
#         - ADV
#         # - AUX
#         # - CONJ
#         # - CCONJ
#         # - DET
#         # - INTJ
#         - NOUN
#         # - NUM
#         # - PART
#         # - PRON
#         # - PROPN
#         # - PUNCT
#         # - SCONJ
#         # - SYM
#         - VERB
#         # - X
#         # - SPACE
#     exclude_entity_types:
#         - CARDINAL
#         - TIME
#         - PERCENT
#         - MONEY
#         # - DATE
#         # - QUANTITY
#         # - ORDINAL
#     min_token_length: 2
#     max_token_length: 50
#     cleaner:
#         # Options for cleaning.corrector.recover_segmented_words
#         fix_fragmented_tokens:
#             use: True
#             params:
#                 max_len: 5
#         # Expand the acronyms in the text
#         expand_acronyms:
#             use: True
#             params: {}
#         # Update the spacy doc with the whitelisted entitiy tag
#         tag_whitelisted_entities:
#             use: True
#             params: {}
#         # Use the part-of-speech as filter
#         filter_by_pos:
#             use: True
#             params: {}
#         # Use extracted entities as filter
#         filter_by_entities:
#             use: True
#             params: {}
#         # Check and fix spelling based on the Respeller module
#         correct_misspelling:
#             use: True
#             params: {}
#         # Remove stopwords from the text
#         filter_stopwords:
#             use: True
#             params: {}
#         # Filter by language
#         filter_language:
#             use: True
#             params:
#                 langs:
#                     - en
#                 score: 0.98

#     spell_checker:
#         __init__:
#             lang: en_US
#             text: null
#             tokenize: null
#             chunkers: null
#             filters: null

#     respeller:
#         __init__:
#             dictionary_file: null
#             spell_threshold: 0.25
#             allow_proper: False  # Don't include proper names in suggestions
#             spell_cache: null
#         infer_correct_word:
#             sim_thresh: 0.0
#             print_log: False
#             min_len: 3
#             use_suggest_score: True
#         infer_correct_words:
#             return_tokens_as_list: True


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


class CleanerConfig(BaseModel):
    # Options for cleaning.corrector.recover_segmented_words
    fix_fragmented_tokens: Params
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
    filter_language: Params
    include_pos_tags: List[POSTag] = [
        POSTag.adjective.value, POSTag.noun.value]
    exclude_entity_types: List[Entity] = [
        Entity.cardinal.value, Entity.time.value]


class POSTagType(BaseModel):
    pos: POSTag


class EntityType(BaseModel):
    ent: Entity


@ router.post("/clean")
async def clean(
        text: str,
        cleaner_config: CleanerConfig,
        spell_checker_config: SpellCheckerConfig,
        respeller_config: RespellerConfig,
        # include_pos_tags: List[str] = [
        #     POSTag.adjective, POSTag.noun],
        # exclude_entity_types: List[str] = [Entity.cardinal, Entity.time]
):
    '''This endpoint accepts configuration parameters and cleans the text data.'''
    spell_checker_config = spell_checker_config.dict()
    respeller_config = respeller_config.dict()
    cleaner_config = cleaner_config.dict()

    spell_checker_config['__init__'] = spell_checker_config.pop('init')
    respeller_config['__init__'] = respeller_config.pop('init')

    cleaner_config['fix_fragmented_tokens']['params']['max_len'] = 5

    cleaner_config['filter_language']['params']['langs'] = ['en']
    cleaner_config['filter_language']['params']['score'] = 0.98

    config = dict(
        cleaner=cleaner_config,
        spell_checker=spell_checker_config,
        respeller=respeller_config)

    config['min_token_length'] = 3
    config['max_token_length'] = 50

    config['include_pos_tags'] = [
        p.value for p in cleaner_config.pop('include_pos_tags')]
    config['exclude_entity_types'] = [
        e.value for e in cleaner_config.pop('exclude_entity_types')]

    cleaner_object = cleaner.BaseCleaner(
        config=config,
        include_pos=config['include_pos_tags'],
        exclude_entities=config['exclude_entity_types'],
        min_token_length=config['min_token_length'],
        max_token_length=config['max_token_length']
    )

    cleaned_text = cleaner_object.get_clean_tokens(text)
    print(cleaned_text)

    return dict(
        text=text,
        cleaned_text=cleaned_text,
        cleaner_config=config)

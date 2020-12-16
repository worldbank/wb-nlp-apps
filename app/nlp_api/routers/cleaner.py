'''This router contains the implementation for the cleaning API.
'''
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/cleaner",
    tags=["cleaner"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


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


@ router.post("/clean")
async def clean(
        text: str,
        cleaner_config: CleanerConfig,
        spell_checker_config: SpellCheckerConfig,
        respeller_config: RespellerConfig):
    '''This endpoint accepts configuration parameters and cleans the text data.'''

    return dict(
        text=text,
        cleaner_config=cleaner_config,
        spell_checker_config=spell_checker_config,
        respeller_config=respeller_config)

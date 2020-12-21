from wb_nlp.utils.data_types import HashableDict
from wb_nlp.cleaning import cleaner
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Body
from functools import lru_cache
from typing import Optional, List
import enum
from typing import List, Any

from pydantic import BaseModel
from wb_nlp.utils.scripts import generate_model_hash


class SpaCyPOSTag(enum.Enum):
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


class LanguageFilter(BaseModel):
    lang: str
    score: float


class CleanerFlags(BaseModel):
    expand_acronyms: bool = True
    tag_whitelisted_entities: bool = True
    correct_misspelling: bool = True
    filter_stopwords: bool = True
    fix_fragmented_tokens: bool = True
    filter_language: bool = True
    include_pos_tags: bool = True
    exclude_entity_types: bool = True
    filter_language: bool = True


class CleanerParams(BaseModel):
    include_pos_tags__pos: List[SpaCyPOSTag] = []
    exclude_entity_types__entities: List[Entity] = []
    fix_fragmented_tokens__max_len: int = 5
    filter_language__langs: List[LanguageFilter] = [
        LanguageFilter(lang='en', score=0.98)]


class Cleaner(BaseModel):
    config_id: str = ''
    flags: CleanerFlags = CleanerFlags(
        expand_acronyms=True,
        tag_whitelisted_entities=True,
        correct_misspelling=True,
        filter_stopwords=True,
        fix_fragmented_tokens=True,
        filter_language=True,
        include_pos_tags=True,
        exclude_entity_types=True,
    )
    params: CleanerParams = CleanerParams()
    min_token_length: int = 3
    max_token_length: int = 50

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.config_id = generate_model_hash(self.dict())


'''This router contains the implementation for the cleaning API.
'''


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

    # class Config:
    #     schema_extra = {
    #         "example": "Example"
    #     }


class POSTagType(BaseModel):
    pos: POSTag


class EntityType(BaseModel):
    ent: Entity

############# END: DEFINITION OF DATA TYPES AND MODELS #############


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

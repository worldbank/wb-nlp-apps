'''
This module contains the type definitions for the configuration parameters
of the cleaning pipeline.

This typed data structure will be used in the implementation of the API using
FastAPI.
'''

import enum
import json
from typing import List, Any
from pydantic import BaseModel, Field, validator
from wb_nlp.utils.scripts import generate_model_hash


class SpaCyPOSTag(str, enum.Enum):
    '''Enum of SpaCy part-of-speech tags.
    '''
    # SpaCy pos tags
    adjective = "ADJ"
    adposition = "ADP"
    adverb = "ADV"
    auxiliary = "AUX"
    conjunction = "CONJ"
    coordinating_conjunction = "CCONJ"
    determiner = "DET"
    interjection = "INTJ"
    noun = "NOUN"
    numeral = "NUM"
    particle = "PART"
    pronoun = "PRON"
    proper_noun = "PROPN"
    punctuation = "PUNCT"
    subordinating_conjunction = "SCONJ"
    symbol = "SYM"
    verb = "VERB"
    other = "X"
    space = "SPACE"

    class Config:
        use_enum_values = True


class Entity(str, enum.Enum):
    '''Enum of SpaCy entities.
    '''
    cardinal = "CARDINAL"           # Numerals that do not fall under another type.
    time = "TIME"                   # Times smaller than a day.
    percent = "PERCENT"             # Percentage, including ”%“.
    money = "MONEY"                 # Monetary values, including unit.
    date = "DATE"                   # Absolute or relative dates or periods.
    quantity = "QUANTITY"           # Measurements, as of weight or distance.
    ordinal = "ORDINAL"             # “first”, “second”, etc.
    language = "LANGUAGE"           # Any named language.
    law = "LAW"                     # Named documents made into laws.
    work_of_art = "WORK_OF_ART"     # Titles of books, songs, etc.

    # Named hurricanes, battles, wars, sports events, etc.
    event = "EVENT"
    # Objects, vehicles, foods, etc. (Not services.)
    product = "PRODUCT"
    # Non-GPE locations, mountain ranges, bodies of water.
    loc = "LOC"
    gpe = "GPE"                     # Countries, cities, states.
    org = "ORG"                     # Companies, agencies, institutions, etc.
    # Buildings, airports, highways, bridges, etc.
    fac = "FAC"
    # Nationalities or religious or political groups.
    norp = "NORP"
    person = "PERSON"               # People, including fictional.

    class Config:
        use_enum_values = True


class LanguageFilter(BaseModel):
    """Data type for language detection.
    """
    lang: str = Field(
        ...,
        description="Language code as defined in enchant library.")
    score: float = Field(
        ...,
        description="Threshold score for a detected language to be considered as significant."
    )

    def __gt__(self, other):
        # Add this so that we could sort this class later.
        return self.lang > other.lang

    # def __eq__(self, other):
    #     return self.lang == other.lang

    def __lt__(self, other):
        # Add this so that we could sort this class later.
        return self.lang < other.lang


class CleanerFlags(BaseModel):
    """Container of flags that control the
    behavior of the cleaning pipeline.
    """
    correct_misspelling: bool = True
    exclude_entity_types: bool = True
    expand_acronyms: bool = True
    filter_stopwords: bool = True
    filter_language: bool = True
    fix_fragmented_tokens: bool = True
    include_pos_tags: bool = True
    tag_whitelisted_entities: bool = True


class CleanerParams(BaseModel):
    '''Definition of parameters for the cleaner pipeline.
    '''
    entities: List[Entity] = Field(
        ...,
        description="List of SpaCy entity types to be `excluded` in the cleaned text. The `exclude_entity_types` flag must be set to `True` before this takes effect.")

    fragmented_token_max_len: int = Field(
        5, description="Maximum number of tokens to consider for fixing fragmented lines of text. The `fix_fragmented_tokens` flag must be set to `True` before this takes effect.")

    languages: List[LanguageFilter] = Field(
        [LanguageFilter(lang='en', score=0.98)],
        description="List of languages code defined in the `pyenchant` library that will be considered as valid. The `filter_language` flag must be set to `True` before this takes effect.")

    max_token_length: int = Field(
        50, description="Maximum character limit for a token to be considered as valid.")

    min_token_length: int = Field(
        3, ge=2, description="Minimum character limit for a token to be considered as valid.")

    pos_tags: List[SpaCyPOSTag] = Field(
        ...,
        description="List of SpaCy part-of-speech tags to be `included` in the cleaned text. The `include_pos_tags` flag must be set to `True` before this takes effect.")

    @validator('entities')
    def sort_entities(cls, v):
        return sorted(v)

    @validator('languages')
    def sort_languages(cls, v):
        return sorted(v)

    @validator('pos_tags')
    def sort_pos_tags(cls, v):
        return sorted(v)

    @validator('max_token_length', pre=True, always=True)
    def max_token_length_greater_than_min(cls, v, values, **kwargs):
        if 'min_token_length' in values and v <= values['min_token_length']:
            raise ValueError(
                '`max_token_length` must be greater than `min_token_length`!')
        return v

    @validator('min_token_length', pre=True, always=True)
    def min_token_length_less_than_max(cls, v, values, **kwargs):
        if 'max_token_length' in values and v >= values['max_token_length']:
            raise ValueError(
                '`min_token_length` must be less than `max_token_length`!')
        return v


class Cleaner(BaseModel):
    """Main cleaner configuration body that contains the specification
    for the flags and parameters that will be used in the cleaning process.
    """
    cleaner_config_id: str = Field(
        '', description="Cleaner configuration id derived from the combination of the parameters.")
    flags: CleanerFlags = CleanerFlags(
        expand_acronyms=True,
        correct_misspelling=True,
        filter_stopwords=True,
        fix_fragmented_tokens=True,
        filter_language=True,
        include_pos_tags=True,
        exclude_entity_types=True,
        tag_whitelisted_entities=True,
    )
    params: CleanerParams = CleanerParams(
        pos_tags=[SpaCyPOSTag.noun, SpaCyPOSTag.adverb,
                  SpaCyPOSTag.verb, SpaCyPOSTag.adjective],
        entities=[
            Entity.cardinal,
            Entity.money,
            Entity.time,
            Entity.percent],
        languages=[LanguageFilter(
            lang='en', score=0.98)]
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'cleaner_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('cleaner_config_id')

        super().__init__(**temp_data)

        self.cleaner_config_id = generate_model_hash(json.loads(self.json()))


class RespellerInferCorrectWord(BaseModel):
    sim_thresh: float = Field(0.0, ge=0, le=1, description="")
    print_log: bool = Field(False, description="")
    min_len: int = Field(3, description="")
    use_suggest_score: bool = Field(True, description="")


class RespellerInferCorrectWords(BaseModel):
    infer_correct_word_params: RespellerInferCorrectWord = Field(
        RespellerInferCorrectWord(),
        description="Set of parameters for the `infer_correct_word` method.")
    return_tokens_as_list: bool = Field(
        True, description="Flag that controls whether the returned value will be a list of tokens or concatenation of the tokens as a single space separated string.")


class Respeller(BaseModel):
    respeller_config_id: str = Field(
        '', description="Respeller configuration id derived from the combination of the parameters.")
    dictionary_file: str = Field(None)
    spell_threshold: float = Field(0.25)
    allow_proper: bool = Field(True)
    spell_cache: dict = Field(None)
    infer_correct_words: RespellerInferCorrectWords = Field(
        RespellerInferCorrectWords(),
        description="Set of parameters for the `infer_correct_words` method.")

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'respeller_config_id' in temp_data:
            # Remove `respeller_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('respeller_config_id')

        super().__init__(**temp_data)

        self.respeller_config_id = generate_model_hash(json.loads(self.json()))


class SpellChecker(BaseModel):
    spell_checker_config_id: str = Field(
        '', description="SpellChecker configuration id derived from the combination of the parameters.")
    lang: str = 'en_US'
    text: Any = None
    tokenize: Any = None
    chunkers: Any = None
    filters: Any = None

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'spell_checker_config_id' in temp_data:
            # Remove `spell_checker_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('spell_checker_config_id')

        super().__init__(**temp_data)

        self.spell_checker_config_id = generate_model_hash(
            json.loads(self.json()))


class CleaningConfig(BaseModel):
    cleaning_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")
    cleaner: Cleaner = Field(
        Cleaner(),
        description="Parameters for the cleaning pipeline."
    )
    respeller: Respeller = Field(
        Respeller(),
        description="Parameters for the respelling algorithm.")
    spell_checker: SpellChecker = Field(
        SpellChecker(),
        description="Parameters for the spell checking algorithm.")
    meta: Any = Field(
        None, description="Metadata that may provide additional information about the cleaner."
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'cleaning_config_id' in temp_data:
            # Remove `cleaning_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('cleaning_config_id')

        super().__init__(**temp_data)

        self.cleaning_config_id = generate_model_hash(json.loads(self.json()))

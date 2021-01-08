'''
This module contains the type definitions for the configuration parameters
of the model inference.

This typed data structure will be used in the implementation of the API using
FastAPI.
'''

import enum
from typing import List, Any
from pydantic import BaseModel, Field, validator
from wb_nlp.utils.scripts import generate_model_hash
from fastapi import File, UploadFile


class ModelTypes(enum.Enum):
    '''Types of models available.
    '''
    lda = "lda"  # Gensim LDA implementation
    mallet = "mallet"  # Mallet LDA implementation
    word2vec = "word2vec"  # Gensim Word2vec implementation


class Word2VecTransformParams(BaseModel):
    raw_text: str = Field(
        '', description="Input text to transform. If a file is uploaded, this will be ignored.")
    # file: UploadFile = File(None, description='File to upload.')
    model_id: str = Field(
        ..., description="Identification of the desired model configuration to use for the operation. The cleaning pipeline associated with this model will also be applied.")
    model_type: ModelTypes = Field(
        ModelTypes.lda, description="Model type. Set as LDA model.")
    topn_words: int = Field(
        10, ge=1, description='Number of similar words to return.')
    topn_docs: int = Field(
        10, ge=1, description='Number of similar docs to return.')

    show_duplicates: bool = Field(
        False, description='Flag that indicates whether to return highly similar or possibly duplicate documents.'
    )
    duplicate_threshold: float = Field(
        0.98, ge=0, description='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
    )
    return_related_words: bool = Field(
        True, description='Flag indicating an option to return similar or topic words to the document.')
    translate: bool = Field(
        True, description='Flag indicating an option to translate the input data.'
    )


class LDATransformParams(BaseModel):
    raw_text: str = Field(
        '', description="Input text to transform. If a file is uploaded, this will be ignored.")
    # file: UploadFile = File(None, description='File to upload.')
    model_id: str = Field(
        ..., description="Identification of the desired model configuration to use for the operation. The cleaning pipeline associated with this model will also be applied.")
    model_type: ModelTypes = Field(
        ModelTypes.lda, description="Model type. Set as LDA model.")
    topn_words: int = Field(
        10, ge=1, description='Number of similar words to return.')
    topn_docs: int = Field(
        10, ge=1, description='Number of similar docs to return.')
    show_duplicates: bool = Field(
        False, description='Flag that indicates whether to return highly similar or possibly duplicate documents.'
    )
    duplicate_threshold: float = Field(
        0.98, ge=0, description='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
    )
    topic_id: int = Field(
        0, description="Topic id of interest."
    )
    topn_topics: int = Field(
        10, ge=1, description='Return at most `topn_topics` topics.')
    topn_topic_words: int = Field(
        10, ge=1, description='Return at most `topn_topic_words` words in topic.')

    total_topic_score: float = Field(
        0.8, ge=0, description="Return at most `total_topic_score` cumulative proportion topics."
    )
    total_word_score: float = Field(
        0.8, description="Return at most `total_word_score` cumulative proportion words in topic."
    )

    translate: bool = Field(
        True, description='Flag indicating an option to translate the input data.'
    )

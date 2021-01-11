# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
import enum
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, validator

from wb_nlp.types.metadata_enums import (
    AdminRegions,
    Corpus,
    GeographicRegions
)


class MetadataModel(BaseModel):
    hex_id: str
    int_id: int

    adm_region: List[AdminRegions] = Field(
        None,
        description="List of administrative regions. Example: Africa."
    )
    author: Optional[List[str]]

    collection: str
    corpus: List[Corpus]
    country: Optional[List[str]]

    date_published: date
    digital_identifier: str = Field(
        None,
        description="Document digital identifier. For WB documents, use the information from API; for other corpus, use ISBN, or DOI, or other ID if available."
    )
    doc_type: str

    filename_original: str = Field(
        ..., description="Filename of the document without path."
    )

    geo_region: List[GeographicRegions] = Field(
        None, description="List of geographic regions covered in the document."
    )

    title: str
    url_txt: str
    url_pdf: str

    year: int

    major_doc_type: str

    journal: str
    volume: str

    language_src: str

    topics_src: List[str] = Field(
        None,
        description="Raw topics extracted from source."
    )

    der_language: str
    der_language_score: float
    der_raw_token_count: int

    der_countries: List[str] = Field(
        None,
        description="List of extracted countries from the document."
    )

    der_acronyms: List[str] = Field(
        None,
        description="List of extracted acronyms from the document."
    )

    wb_topics: Optional[list]
    wb_doc_type: str


class DocumentModel(BaseModel):
    text: str

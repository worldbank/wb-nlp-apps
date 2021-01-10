# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, validator


class MetadataModel(BaseModel):
    hex_id: str
    int_id: int

    title: str
    url_txt: str
    url_pdf: str

    corpus: str
    year: int

    major_doc_type: str
    doc_type: str

    collection: str
    journal: str
    volume: str

    date_published: date

    digital_identifier: str = Field(
        None,
        description="Document digital identifier. For WB documents, use the information from API; for other corpus, use ISBN, or DOI, or other ID if available."
    )

    language_src: str

    topics_src: List[str] = Field(
        None,
        description="Raw topics extracted from source."
    )

    adm_region: List[str] = Field(
        None,
        description="List of administrative regions. Example: Africa."
    )

    countries: Optional[list]
    author: Optional[list]

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

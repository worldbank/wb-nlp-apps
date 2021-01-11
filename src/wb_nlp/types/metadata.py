# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
import enum
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator, AnyUrl

from wb_nlp.types.metadata_enums import (
    WBAdminRegions,
    Corpus,
    WBDocTypes,
    WBGeographicRegions,
    WBMajorDocTypes,
    WBTopics,
    WBSubTopics,
)


class MetadataModel(BaseModel):
    hex_id: str = Field(
        ..., description=""
    )
    int_id: int = Field(
        ..., description=""
    )

    adm_region: List[WBAdminRegions] = Field(
        None, description="List of administrative regions. Example: Africa."
    )
    author: List[str] = Field(
        None, description=""
    )

    cleaning_config_id: str = Field(
        None,
        description="This corresponds to the configuration ID of the cleaning pipeline that was used to generate the cleaned file in the `path_clean` field."
    )
    collection: str = Field(
        None, description=""
    )
    corpus: Corpus = Field(
        ..., description=""
    )
    country: List[str] = Field(
        None, description=""
    )

    date_published: date = Field(
        None, description=""
    )
    der_acronyms: List[str] = Field(
        None, description="List of extracted acronyms from the document."
    )
    der_countries: List[str] = Field(
        None, description="List of extracted countries from the document."
    )
    der_language_detected: str = Field(
        None, description=""
    )
    der_language_score: float = Field(
        None, description=""
    )
    der_raw_token_count: int = Field(
        None, description=""
    )
    der_clean_token_count: int = Field(
        None, description=""
    )
    digital_identifier: str = Field(
        None,
        description="Document digital identifier. For WB documents, use the information from API; for other corpus, use ISBN, or DOI, or other ID if available."
    )
    doc_type: List[WBDocTypes] = Field(
        None, description=""
    )

    filename_original: str = Field(
        ..., description="Filename of the document without path."
    )

    geo_region: List[WBGeographicRegions] = Field(
        None, description="List of geographic regions covered in the document."
    )

    journal: str = Field(
        None, description=""
    )

    # language_detected -> der_language_detected
    # language_score -> der_language_score

    language_src: str = Field(
        None, description=""
    )
    last_update_date: datetime

    major_doc_type: List[WBMajorDocTypes] = Field(
        None, description=""
    )

    path_clean: str = Field(
        None, description=""
    )
    path_original: str = Field(
        ..., description=""
    )

    title: str = Field(
        ..., description=""
    )
    # tokens -> der_clean_token_count
    topics_src: List[WBTopics] = Field(
        None, description="Raw topics extracted from source."
    )

    url_pdf: AnyUrl = Field(
        None, description=""
    )
    url_txt: AnyUrl = Field(
        None, description=""
    )

    volume: str = Field(
        None, description=""
    )

    wb_lending_instrument: str = Field(
        None, description=""
    )
    wb_major_theme: str = Field(
        None, description=""
    )
    wb_product_line: str = Field(
        None, description=""
    )
    wb_project_id: str = Field(
        None, description=""
    )
    wb_sector: str = Field(
        None, description=""
    )
    wb_subtopic_src: List[WBSubTopics] = Field(
        None, description=""
    )
    wb_theme: str = Field(
        None, description=""
    )
    year: int


class DocumentModel(BaseModel):
    text: str

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
import enum
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator, AnyUrl
from hashlib import md5
from dateutil import parser

from wb_nlp.types.metadata_enums import (
    WBAdminRegions,
    Corpus,
    WBDocTypes,
    WBGeographicRegions,
    WBMajorDocTypes,
    WBTopics,
    # WBSubTopics,  # Don't normalize subtopics since we don't have a reliable curated list yet.
)


def make_list_or_null(value, delimiter):
    value = value.split(delimiter)
    if value == ['']:
        value = None

    return value


def migrate_nlp_schema(body):
    """This method updates the data under the previous schema into
    the pydantic MetadataModel schema.
    """
    body = dict(body)

    body["hex_id"] = md5(body['_id'].encode('utf-8')).hexdigest()[:15]
    body["int_id"] = int(body["hex_id"], 16)

    body["adm_region"] = make_list_or_null(
        body["adm_region"], delimiter=WBAdminRegions.delimiter)
    body["author"] = make_list_or_null(body["author"], delimiter=",")

    body["corpus"] = body["corpus"].upper()
    body["country"] = make_list_or_null(body["country"], delimiter=",")

    body["date_published"] = parser.parse(
        body["date_published"]).date() or None

    body["der_countries"] = body.get("countries") or None

    body["der_language_detected"] = body.get("language_detected") or None
    body["der_language_score"] = body.get("language_score") or None

    body["der_clean_token_count"] = body.get("tokens") or None

    body["doc_type"] = make_list_or_null(
        body["doc_type"], delimiter=WBDocTypes.delimiter)

    body["geo_region"] = make_list_or_null(
        body["geo_region"], delimiter=WBGeographicRegions.delimiter)

    body["last_update_date"] = datetime.now()

    body["major_doc_type"] = make_list_or_null(
        body["major_doc_type"], delimiter=WBMajorDocTypes.delimiter)

    body["topics_src"] = make_list_or_null(
        body["topics_src"].replace(
            "Health, Nutrition and Population",
            "Health; Nutrition and Population"),
        delimiter=WBTopics.delimiter)

    body["url_pdf"] = body["url_pdf"] or None
    body["url_txt"] = body["url_txt"] or None

    body["wb_subtopic_src"] = make_list_or_null(
        body["wb_subtopic_src"], delimiter=",")

    return MetadataModel(**body)


class CountryCounts(BaseModel):
    country_code: str
    count: int


class MetadataModel(BaseModel):
    """
    Summary of required fields:
        - hex_id
        - int_id
        - corpus
        - filename_original
        - last_update_date
        - path_original
        - title
    """
    hex_id: str = Field(
        ..., description="This id will be the basis for the `int_id` that will be used in the Milvus index.")
    int_id: int = Field(
        ..., description="This will be the id derived from the `hex_id` that will be used in the Milvus index.")

    adm_region: List[WBAdminRegions] = Field(
        None, description="List of administrative regions. Example: Africa.")
    author: List[str] = Field(
        None, description="")

    cleaning_config_id: str = Field(
        None,
        description="This corresponds to the configuration ID of the cleaning pipeline that was used to generate the cleaned file in the `path_clean` field.")
    collection: str = Field(
        None, description="")
    corpus: Corpus = Field(
        ..., description="")
    country: List[str] = Field(
        None, description="")

    date_published: date = Field(
        None, description="")
    der_acronyms: List[str] = Field(
        None, description="Frequency of extracted acronyms from the document.")
    der_countries: dict = Field(
        None, description="Frequency of extracted countries from the document.")
    der_language_detected: str = Field(
        None, description="")
    der_language_score: float = Field(
        None, description="")
    der_raw_token_count: int = Field(
        None, description="")
    der_clean_token_count: int = Field(
        None, description="")
    digital_identifier: str = Field(
        None,
        description="Document digital identifier. For WB documents, use the information from API; for other corpus, use ISBN, or DOI, or other ID if available.")
    doc_type: List[WBDocTypes] = Field(
        None, description="")

    filename_original: str = Field(
        ..., description="Filename of the document without path.")

    geo_region: List[WBGeographicRegions] = Field(
        None, description="List of geographic regions covered in the document.")

    journal: str = Field(
        None, description="")

    # language_detected -> der_language_detected
    # language_score -> der_language_score

    language_src: str = Field(
        None, description="")
    last_update_date: datetime = Field(
        ..., description="")

    major_doc_type: List[WBMajorDocTypes] = Field(
        None, description="")

    path_clean: str = Field(
        None, description="")
    path_original: str = Field(
        ..., description="")

    title: str = Field(
        ..., description="")
    # tokens -> der_clean_token_count
    topics_src: List[WBTopics] = Field(
        None, description="Raw topics extracted from source.")

    url_pdf: AnyUrl = Field(
        None, description="")
    url_txt: AnyUrl = Field(
        None, description="")

    volume: str = Field(
        None, description="")

    wb_lending_instrument: str = Field(
        None, description="")
    wb_major_theme: str = Field(
        None, description="")
    wb_product_line: str = Field(
        None, description="")
    wb_project_id: str = Field(
        None, description="")
    wb_sector: str = Field(
        None, description="")
    wb_subtopic_src: List[str] = Field(
        None, description="")
    wb_theme: str = Field(
        None, description="")

    year: int = Field(
        None, description="")


class DocumentModel(BaseModel):
    text: str

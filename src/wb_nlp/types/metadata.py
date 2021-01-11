# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
import enum
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, validator


def get_wb_curated_list(list_id):
    """Enumerates the list of items corresponding to the given `list_id` found in the
    World Bank's wds API.

    Source: https://search.worldbank.org/api/v2/wds

    Example:
        list_id = "geo_reg"
    """
    import re
    import requests
    from bs4 import BeautifulSoup

    r = requests.get('https://search.worldbank.org/api/v2/wds')
    b = BeautifulSoup(r.content, 'html.parser')

    item_list = b.find('select', id=list_id).find_all('option')
    g = {re.sub(r'[^a-z]+', '_', o.text.lower()): o.text for o in item_list}

    for k, v in g.items():
        print(f'{k} = "{v}"')


class GeographicRegions(enum.Enum):
    '''Curated list of geographic regions.
    '''
    africa = "Africa"
    america = "America"
    asia = "Asia"
    caribbean = "Caribbean"
    central_africa = "Central Africa"
    central_america = "Central America"
    central_asia = "Central Asia"
    commonwealth_of_independent_states = "Commonwealth of Independent States"
    east_africa = "East Africa"
    east_asia = "East Asia"
    eastern_europe = "Eastern Europe"
    europe = "Europe"
    europe_and_central_asia = "Europe and Central Asia"
    europe_middle_east_and_north_africa = "Europe, Middle East and North Africa"
    european_union = "European Union"
    latin_america = "Latin America"
    middle_east = "Middle East"
    north_africa = "North Africa"
    north_america = "North America"
    oceania = "Oceania"
    sahel = "Sahel"
    south_america = "South America"
    south_asia = "South Asia"
    southeast_asia = "Southeast Asia"
    southern_africa = "Southern Africa"
    sub_saharan_africa = "Sub-Saharan Africa"
    west_africa = "West Africa"
    world = "World"


class AdminRegions(enum.Enum):
    '''Curated list of administrative regions.
    '''
    africa = "Africa"
    africa_east = "Africa East"
    africa_west = "Africa West"
    east_asia_and_pacific = "East Asia and Pacific"
    europe_and_central_asia = "Europe and Central Asia"
    latin_america_caribbean = "Latin America & Caribbean"
    latin_america_amp_caribbean = "Latin America &amp; Caribbean"
    middle_east_and_north_africa = "Middle East and North Africa"
    oth = "OTH"
    other = "Other"
    others = "Others"
    rest_of_the_world = "Rest Of The World"
    south_asia = "South Asia"
    the_world_region = "The World Region"


class MetadataModel(BaseModel):
    hex_id: str
    int_id: int

    adm_region: List[AdminRegions] = Field(
        None,
        description="List of administrative regions. Example: Africa."
    )
    author: Optional[List[str]]

    collection: str
    corpus: str
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

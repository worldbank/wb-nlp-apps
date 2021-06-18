'''This router contains the implementation for the cleaning API.
'''
from functools import lru_cache
from fastapi import APIRouter
import requests


router = APIRouter(
    prefix="/microdata",
    tags=["Microdata metadata"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def _get_study_info(idno):

    metadata = _get_microdata_metadata(idno)
    return dict(dataset=dict(metadata=dict(study_desc=dict(study_info=metadata.get(
        "dataset", {}).get("metadata", {}).get("study_desc", {}).get("study_info")))))


@lru_cache(maxsize=512)
def _get_microdata_metadata(idno):
    try:
        url = f"https://catalog.ihsn.org/api/catalog/{idno}"
        response = requests.get(url)
    except:
        url = f"https://microdatalib.worldbank.org/api/catalog/{idno}"
        response = requests.get(url)

    response = response.json()

    return response


@ router.get("/get_microdata_metadata/{idno}")
async def get_microdata_metadata(idno: str):
    '''This provides an interface to the IHSN microdata catalog API.
    '''
    data = None
    try:
        data = _get_microdata_metadata(idno)
    except Exception as e:
        pass

    return data


@ router.get("/get_microdata_study_info/{idno}")
async def get_microdata_study_info(idno: str):
    '''This provides an interface to the IHSN microdata catalog's API study info.
    '''
    data = None
    try:
        data = _get_study_info(idno)
    except Exception as e:
        pass

    return data

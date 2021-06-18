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


@lru_cache(maxsize=512)
def _get_microdata_metadata(idno):
    url = f"https://catalog.ihsn.org/api/catalog/{idno}"
    response = requests.get(url)
    response = response.json()
    return response


@ router.get("/get_microdata_metadata/{idno}")
async def get_microdata_metadata(idno: str):
    '''This provides an interface to the ihsn microdata catalog API.
    '''
    data = None
    try:
        data = _get_microdata_metadata(idno)
    except Exception as e:
        pass

    return data

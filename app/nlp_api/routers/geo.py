'''This router contains the implementation for the cleaning API.
'''
from fastapi import APIRouter
from wb_cleaning.extraction import country_extractor


router = APIRouter(
    prefix="/geo",
    tags=["Geographic data"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_country_groups_names")
async def get_country_groups_names():
    """This returns the mapping of country groups to their expanded names.
    """
    return dict(country_groups_names=country_extractor.country_groups_names)


@ router.get("/get_country_region_colors")
async def get_country_region_colors():
    """This returns the mapping of country groups to their expanded names.
    """
    return dict(country_region_colors=country_extractor.COUNTRY_REGION_COLORS)

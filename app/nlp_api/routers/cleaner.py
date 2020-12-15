'''This router contains the implementation for the cleaning API.
'''
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/cleaner",
    tags=["cleaner"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@router.get("/clean")
async def clean():
    return {}

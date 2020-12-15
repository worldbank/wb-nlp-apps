from typing import Optional
from enum import Enum

from fastapi import FastAPI

from nlp_api.routers import cleaner

app = FastAPI()

app.include_router(cleaner.router)


@app.get("/")
def read_root():
    return {"NLP App": "Root"}

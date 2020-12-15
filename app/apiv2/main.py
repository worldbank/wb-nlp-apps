from typing import Optional
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"NLP App": "Root"}

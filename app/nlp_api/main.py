from typing import Optional
from enum import Enum
import uvicorn
from fastapi import FastAPI

from .routers import cleaner, models

app = FastAPI()

app.include_router(cleaner.router)
app.include_router(models.router)


@app.get("/")
def read_root():
    return {"NLP App": "Root"}


if __name__ == '__main__':
    # Default port is 8000
    # uvicorn app.nlp_api.main:app --reload --timeout-keep-alive 120 --port 8919
    uvicorn.run(app, port=8919, host='0.0.0.0')

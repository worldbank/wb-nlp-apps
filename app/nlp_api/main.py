from typing import Optional
from enum import Enum
import uvicorn
from fastapi import FastAPI

from .routers import cleaner, models, metadata
from .routers.subrouters import lda, word2vec

app = FastAPI()

app.include_router(metadata.corpus)
app.include_router(cleaner.router)
app.include_router(models.router)
app.include_router(
    word2vec.router,
    prefix="/models",
    # tags=["word2vec"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    lda.router,
    prefix="/models",
    # tags=["lda"],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
def read_root():
    return {"NLP App": "Root"}


if __name__ == '__main__':
    # Default port is 8000
    # uvicorn app.nlp_api.main:app --reload --timeout-keep-alive 120 --port 8919
    uvicorn.run(app, port=8919, host='0.0.0.0')

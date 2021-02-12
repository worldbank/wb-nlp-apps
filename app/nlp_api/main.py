from typing import Optional
from enum import Enum
import uvicorn
from fastapi import FastAPI

from .routers import cleaner, models, metadata
from .routers.subrouters import lda, word2vec

tags_metadata = [
    {
        "name": "Corpus",
        "description": "This collection of endpoints provide access to the documents and metadata scraped from various sources of international development organizations and multilateral development banks.",
    },
    {
        "name": "Cleaner",
        "description": "This collection of endpoints provide interfaces to the cleaning services available in the project's cleaning pipeline.",
    },
    {
        "name": "Models",
        "description": "This collection of endpoints provide interfaces to gather general information on available models.",
    },
    {
        "name": "Word2vec Model",
        "description": "This collection of endpoints provide interfaces to the services built with the word2vec model.",
    },
    {
        "name": "LDA Model",
        "description": "This collection of endpoints provide interfaces to the services built with the LDA model.",
    },
]

app = FastAPI(
    title="KCP/JDC NLP API",
    description="The KCP/JDC NLP REST API provides a suite of endpoints to interact with the underlying data via the `/corpus` enpoints, cleaning pipelines via the `/cleaner` endpoints, and NLP models via the `/models` endpoint of the KCP/JDC project.",
    version="2.5.0",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",  # Set to `None` to disable
)

app.include_router(metadata.router, prefix="/nlp")
app.include_router(cleaner.router, prefix="/nlp")
app.include_router(models.router, prefix="/nlp")
# app.include_router(
#     word2vec.router,
#     prefix="/models",
#     # tags=["word2vec"],
#     responses={404: {"description": "Not found"}},
# )
app.include_router(
    lda.router,
    prefix="/nlp/models",
    # tags=["lda"],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
def read_root():
    return {"NLP App": "Root"}


if __name__ == '__main__':
    # Default port is 8000
    # uvicorn app.nlp_api.main:app --reload --timeout-keep-alive 120 --host 0.0.0.0 --port 8919
    uvicorn.run(app, port=8919, host='0.0.0.0')

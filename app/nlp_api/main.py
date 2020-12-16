from typing import Optional
from enum import Enum
import uvicorn
from fastapi import FastAPI

from .routers import cleaner

app = FastAPI()

app.include_router(cleaner.router)


@app.get("/")
def read_root():
    return {"NLP App": "Root"}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

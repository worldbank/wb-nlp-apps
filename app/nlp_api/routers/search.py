'''This router contains the implementation for the cleaning API.
'''
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, Form
import pydantic

from wb_nlp.interfaces import mongodb, elasticsearch

from wb_nlp.types.models import (
    ModelTypes
)
from ..common.utils import get_validated_model, read_uploaded_file


router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/keyword")
async def keyword_search(
    query: str,
    from_result: int = 0,
    size: int = 10,
):
    '''This endpoint provides the service for the keyword search functionality. This uses Elasticsearch in the backend for the full-text search.
    '''
    response = elasticsearch.text_search(
        query, from_result=from_result, size=size)

    total = response.hits.total.to_dict()
    total["message"] = total["value"]

    return dict(
        total=total,
        hits=[h.to_dict() for h in response.hits],
        next=from_result + size
    )


def common_semantic_search(
        query: str,
        from_result: int = 0,
        size: int = 10,
        clean: bool = True):

    model = get_validated_model(ModelTypes(
        "word2vec"), "777a9cf47411f6c4932e8941f177f90a")

    if clean:
        query = model.clean_text(query)

    result = model.search_similar_documents(
        document=query,
        from_result=from_result,
        size=size)

    id_rank = {res["id"]: res["rank"] for res in result}

    docs_metadata = mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = mongodb.get_docs_metadata_collection()

    response = docs_metadata.find({"id": {"$in": list(id_rank.keys())}})

    total = dict(
        value=None,
        message="many"
    )

    return dict(
        total=total,
        hits=[h for h in sorted(response, key=lambda x: id_rank[x["id"]])],
        next=from_result + size,
        result=result,
    )


@ router.get("/semantic")
async def semantic_search(
    query: str,
    from_result: int = 0,
    size: int = 10,
    clean: bool = True,
):
    '''This endpoint provides the service for the semantic search functionality. This uses a word embedding model to find semantically similar documents in the database.
    '''

    return common_semantic_search(
        query=query, from_result=from_result, size=size, clean=clean)

    # model = get_validated_model(ModelTypes(
    #     "word2vec"), "777a9cf47411f6c4932e8941f177f90a")

    # if clean:
    #     query = model.clean_text(query)

    # result = model.search_similar_documents(
    #     document=query,
    #     from_result=from_result,
    #     size=size)

    # id_rank = {res["id"]: res["rank"] for res in result}

    # docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # # docs_metadata = mongodb.get_docs_metadata_collection()

    # response = docs_metadata.find({"id": {"$in": list(id_rank.keys())}})

    # total = dict(
    #     value=None,
    #     message="many"
    # )

    # return dict(
    #     total=total,
    #     hits=[h for h in sorted(response, key=lambda x: id_rank[x["id"]])],
    #     next=from_result + size,
    #     result=result,
    # )


@ router.post("/file")
async def file_search(
    file: UploadFile = File(...),
    from_result: int = Form(0),
    size: int = Form(10),
    clean: bool = Form(True),
):
    '''This endpoint provides the service for the semantic search functionality. This uses a word embedding model to find semantically similar documents in the database.
    '''
    print({"filename": file.filename})

    # model = get_validated_model(ModelTypes(
    #     "word2vec"), "777a9cf47411f6c4932e8941f177f90a")

    document = read_uploaded_file(file)

    return common_semantic_search(query=document, from_result=from_result, size=size, clean=clean)

    # result = model.search_similar_documents(
    #     document=query,
    #     from_result=from_result,
    #     size=size)

    # id_rank = {res["id"]: res["rank"] for res in result}

    # docs_metadata = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # # docs_metadata = mongodb.get_docs_metadata_collection()

    # response = docs_metadata.find({"id": {"$in": list(id_rank.keys())}})

    # total = dict(
    #     value=None,
    #     message="many"
    # )

    # return dict(
    #     total=total,
    #     hits=[h for h in sorted(response, key=lambda x: id_rank[x["id"]])],
    #     next=from_result + size,
    #     result=result,
    # )

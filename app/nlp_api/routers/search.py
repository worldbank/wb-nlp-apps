'''This router contains the implementation for the cleaning API.
'''
from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import HttpUrl
from contexttimer import Timer
from wb_nlp.interfaces import elasticsearch
from wb_nlp.types.models import (
    ModelTypes
)
from ..common.utils import (
    get_validated_model, read_uploaded_file,
    read_url_file, clean_text, check_translate_keywords
)


router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.post("/keyword")
async def keyword_search(
    query: str,
    author: List[str] = None,
    country: List[str] = None,
    corpus: List[str] = None,
    major_doc_type: List[str] = None,
    adm_region: List[str] = None,
    geo_region: List[str] = None,
    topics_src: List[str] = None,
    from_result: int = 0,
    size: int = 10,
):
    '''This endpoint provides the service for the keyword search functionality. This uses Elasticsearch in the backend for the full-text search.
    '''
    # response = elasticsearch.text_search(
    #     query, from_result=from_result, size=size)

    payload = check_translate_keywords(query)
    query = payload["query"]
    translated = payload["translated"]

    fs = elasticsearch.NLPDocFacetedSearch(query=query, filters=dict(
        author=author,
        country=country,
        corpus=corpus,
        major_doc_type=major_doc_type,
        adm_region=adm_region,
        geo_region=geo_region,
        topics_src=topics_src,
    ))

    response = fs[from_result: from_result + size].execute()

    total = response.hits.total.to_dict()
    total["message"] = total["value"]

    hits = []
    result = []
    highlights = []
    facets = response.aggregations.to_dict()

    for ix, h in enumerate(response, 1):
        hits.append(h.to_dict())
        result.append(dict(id=h.meta.id, rank=ix +
                      from_result, score=h.meta.score))
        try:
            highlight = h.meta.highlight
            highlight["id"] = h.meta.id
        except AttributeError:
            # 'HitMeta' object has no attribute 'highlight'
            highlight["body"] = []
        highlights.append(highlight.to_dict())

    return dict(
        total=total,
        hits=hits,
        result=result,
        highlights=highlights,
        translated=translated,
        facets=facets,
        next=from_result + size
    )


def common_semantic_search(
        model_name: ModelTypes,
        model_id: str,
        query: str,
        from_result: int = 0,
        size: int = 10,
        clean: bool = True,
        translated: dict = None):

    with Timer() as timer:

        print(f"Elapsed 1: {timer.elapsed}")
        model = get_validated_model(model_name, model_id)
        # model = get_validated_model(ModelTypes(
        #     "word2vec"), "777a9cf47411f6c4932e8941f177f90a")

        print(f"Elapsed 2: {timer.elapsed}")
        print("QUERY: ", query[:100])
        if clean:
            query = clean_text(model_name, model_id, query)
            # query = model.clean_text(query)

        # print("CLEANED QUERY: ", query)

        print(f"Elapsed 3: {timer.elapsed}")
        result = model.search_similar_documents(
            document=query,
            from_result=from_result,
            size=size)

        print(f"Elapsed 4: {timer.elapsed}")
        id_rank = {res["id"]: res["rank"] for res in result}

        print(f"Elapsed 5: {timer.elapsed}")
        response = elasticsearch.get_metadata_by_ids(
            doc_ids=list(id_rank.keys()), source_excludes=["body"])

        total = dict(
            value=None,
            message="many"
        )

        print(f"Elapsed 6: {timer.elapsed}")
        hits = [h for h in sorted(response, key=lambda x: id_rank[x["id"]])]

        print(f"Elapsed 7: {timer.elapsed}")

        return dict(
            total=total,
            hits=hits,
            translated=translated,
            next=from_result + size,
            result=result,
        )


@ router.get("/{model_name}/semantic")
async def semantic_search(
    model_name: ModelTypes,
    model_id: str,
    query: str,
    from_result: int = 0,
    size: int = 10,
    clean: bool = False,
):
    '''This endpoint provides the service for the semantic search functionality. This uses a word embedding model to find semantically similar documents in the database.
    '''

    print(model_name, model_id, query)

    payload = check_translate_keywords(query)
    query = payload["query"]
    translated = payload["translated"]

    return common_semantic_search(
        model_name=model_name, model_id=model_id,
        query=query, from_result=from_result, size=size, clean=clean, translated=translated)


@ router.post("/{model_name}/file")
async def file_search(
    model_name: ModelTypes,
    model_id: str = Form(...),
    file: UploadFile = File(...),
    from_result: int = Form(0),
    size: int = Form(10),
    clean: bool = Form(True),
):
    '''This endpoint provides the service for the semantic search functionality. This uses a word embedding model to find semantically similar documents in the database.
    '''
    print({"filename": file.filename})

    document = read_uploaded_file(file)

    return common_semantic_search(model_name=model_name, model_id=model_id, query=document, from_result=from_result, size=size, clean=clean)


@ router.post("/{model_name}/url")
async def url_search(
    model_name: ModelTypes,
    model_id: str = Form(...),
    url: HttpUrl = Form(...),
    from_result: int = Form(0),
    size: int = Form(10),
    clean: bool = Form(True),
):
    '''This endpoint provides the service for the semantic search functionality. This uses a word embedding model to find semantically similar documents in the database.
    '''

    document = read_url_file(url)

    return common_semantic_search(model_name=model_name, model_id=model_id, query=document, from_result=from_result, size=size, clean=clean)

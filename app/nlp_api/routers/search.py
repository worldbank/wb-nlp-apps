'''This router contains the implementation for the cleaning API.
'''
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Query
from pydantic import HttpUrl
from contexttimer import Timer

from wb_cleaning.extraction import country_extractor

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


@ router.get("/get_country_groups_names")
async def get_country_groups_names():
    """This returns the mapping of country groups to their expanded names.
    """
    return dict(country_groups_names=country_extractor.country_groups_names)


@ router.get("/keyword")
async def keyword_search(
    query: str,
    min_year: int = None,
    max_year: int = None,
    author: List[str] = Query(None),
    der_country: List[str] = Query(None),
    der_country_groups: List[str] = Query(None),
    der_regions: List[str] = Query(None),
    der_jdc_tags: List[str] = Query(None),
    corpus: List[str] = Query(None),
    major_doc_type: List[str] = Query(None),
    adm_region: List[str] = Query(None),
    geo_region: List[str] = Query(None),
    topics_src: List[str] = Query(None),
    from_result: int = 0,
    size: int = 10,
    app_tag_jdc: bool = Query(False),
):
    '''This endpoint provides the service for the keyword search functionality. This uses Elasticsearch in the backend for the full-text search.
    '''
    # response = elasticsearch.text_search(
    #     query, from_result=from_result, size=size)
    query_tokens = country_extractor.replace_country_group_names(query).split()

    # country_groups = set()
    # for token in query_tokens:
    #     country_groups.update(
    #         country_extractor.country_groups_map.get(token, []))
    # country_groups = sorted(country_groups)

    der_country_groups = der_country_groups or []
    country_groups = [
        token for token in query_tokens if token in country_extractor.country_groups_map]
    if country_groups:
        # If explicit country group is found in the query, replace the current active filter with it.
        der_country_groups = country_groups

    payload = check_translate_keywords(query)
    query = payload["query"]
    translated = payload["translated"]

    filters = dict(
        author=author or [],
        der_country=der_country or [],
        der_country_groups=der_country_groups or [],
        der_regions=der_regions or [],
        der_jdc_tags=der_jdc_tags or [],
        corpus=corpus or [],
        major_doc_type=major_doc_type or [],
        adm_region=adm_region or [],
        geo_region=geo_region or [],
        topics_src=topics_src or [],
    )

    if min_year:
        if max_year:
            filters["year"] = [datetime(y, 1, 1)
                               for y in range(min_year, max_year + 1)]
            # filters["year"] = [int(datetime(y, 1, 1).timestamp()) * 1000
            #                    for y in range(min_year, max_year + 1)]

        else:
            filters["year"] = [datetime(y, 1, 1)
                               for y in range(min_year, datetime.now().year + 1)]
            # filters["year"] = [int(datetime(y, 1, 1).timestamp()) * 1000
            #                    for y in range(min_year, datetime.now().year + 1)]

    if app_tag_jdc:
        fs = elasticsearch.JDCNLPDocFacetedSearch(query=query, filters=filters)
    else:
        fs = elasticsearch.NLPDocFacetedSearch(query=query, filters=filters)

    response = fs[from_result: from_result + size].execute()

    total = response.hits.total.to_dict()
    total["message"] = total["value"]

    hits = []
    result = []
    highlights = []
    facets = response.aggregations.to_dict()

    for ix, h in enumerate(response, 1):
        highlight = {}
        hits.append(h.to_dict())
        result.append(dict(id=h.meta.id, rank=ix +
                      from_result, score=h.meta.score))
        try:
            highlight = h.meta.highlight.to_dict()
        except AttributeError:
            # 'HitMeta' object has no attribute 'highlight'
            highlight["body"] = []

        highlight["id"] = h.meta.id
        highlights.append(highlight)

    filters["min_year"] = min_year
    filters["max_year"] = max_year

    valid_countries = country_extractor.get_region_countries(der_regions)

    return dict(
        total=total,
        hits=hits,
        result=result,
        highlights=highlights,
        translated=translated,
        facets=facets,
        filters=filters,
        valid_countries=valid_countries,
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


# '_filter_der_country_details_region': {'filter': {'match_all': {}},
#    'aggs': {
#           'der_country_details_region': {'nested': {'path': 'der_country_details'},
#               'aggs': {'inner': {'terms': {'field': 'der_country_details.region',
#         'size': 100,
#         'order': {'metric': 'desc'}},
#        'aggs': {'metric': {'value_count': {'field': 'id'}}}}}}}}

# {
#   "query": {
#     "match_all": {}
#   },
#   "aggs": {
#     "der_country_details": {
#       "nested": {
#         "path": "der_country_details"
#       },
#       "aggs": {
#         "top_regions": {
#           "terms": {
#             "field": "der_country_details.region"
#           },
#           "aggs": {
#             "region_to_doc": {
#               "reverse_nested": {},
#               "aggs": {
#                 "doc_count_per_region": {
#                   "value_count": {
#                     "field": "id"
#                   }
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#   }
# }

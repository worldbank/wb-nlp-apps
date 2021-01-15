'''This router contains the implementation for the cleaning API.
'''
from bson.son import SON
import enum
from datetime import datetime
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body

from wb_nlp.interfaces import mongodb
from wb_nlp.types import metadata
# from wb_nlp.types.metadata_enums import Corpus

router = APIRouter(
    prefix="/corpus",
    tags=["Corpus"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get(
    "/get_metadata_by_id",
    response_model=metadata.MetadataModel,
    summary="Get metadata by id")
def get_doc_metadata_by_id(id: str):
    """This enpoint fetches the metadata corresponding to the given `id`.
    """

    doc = mongodb.get_docs_metadata_collection().find_one({"id": id})
    doc = metadata.MetadataModel(**doc)

    return doc


@router.post(
    "/get_doc_count",
    # response_model=metadata.MetadataModel,
    summary="Get count of documents based on arbitrary grouping fields.")
def get_doc_count(group_fields: List[str] = ["year", "country"], sort_field: dict = {"year": -1, "count": -1}, limit: int = 10):
    """This endpoint provides a generic interface to get a summary count of documents given an arbitrary set of `group_fields`. The return value can be sorted based on the `sort_field` input. The number of returned groups is limited by the `limit` parameter.
    """

    assert len(set(sort_field).difference(group_fields + ['count'])) == 0

    group_id = {b: f"${b}" for b in group_fields}

    sort_field = {f"_id.{s}" if s !=
                  "count" else s: v for s, v in sort_field.items()}
    sort_field = SON(sort_field.items())
    projection = {b: f"$_id.{b}" for b in group_fields}
    projection["count"] = "$count"
    projection["_id"] = 0

    print(projection)

    # Identify fields that needs unwinding, if any
    list_fields = set(["adm_region", "author", "country", "der_acronyms", "doc_type",
                       "geo_region", "major_doc_type", "topics_src", "wb_subtopic_src"])
    unwind_fields = [{"$unwind": f"${b}"}
                     for b in list_fields.intersection(group_fields)]

    pipeline = []

    if unwind_fields:
        pipeline = unwind_fields

    pipeline.extend([
        {"$group": {"_id": group_id, "count": {"$sum": 1}}},
        {"$sort": sort_field},
        {"$limit": limit},
        {"$project": projection},
    ])

    print(pipeline)

    agg = mongodb.get_docs_metadata_collection().aggregate(
        pipeline
    )

    values = list(agg)

    return values


# pipeline = [
#     {"$unwind": "$country"},
#     {"$group": {"_id": {"date_published": "$date_published",
#                         "country": "$country"}, "count": {"$sum": 1}}},
#     {"$sort": SON([("_id.date_published", -1), ("count", -1)])}]


# pipeline = [
#     {"$unwind": "$country"},
#     {"$group": {"_id": {"year": "$year",
#                         "country": "$country"}, "count": {"$sum": 1}}},
#     {"$sort": SON([("_id.year", -1), ("count", -1)])},
#     {"$project": {"_id": 0, "year": "$_id.year",
#                   "country": "$_id.country", "count": "$count"}}
# ]

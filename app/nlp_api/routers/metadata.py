'''This router contains the implementation for the cleaning API.
'''
from bson.son import SON
import enum
from datetime import datetime
from typing import Optional, List
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Body

from wb_nlp.interfaces import mongodb, elasticsearch
from wb_nlp.types import metadata
# from wb_nlp.types.metadata_enums import Corpus

router = APIRouter(
    prefix="/corpus",
    tags=["Corpus"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_corpus_size")
def get_corpus_size():
    """This endpoint gets the current size of the corpus.
    """
    return dict(size=elasticsearch.get_indexed_corpus_size())


@ router.get(
    "/get_metadata_by_id",
    response_model=metadata.MetadataModel,
    summary="Get metadata by id")
def get_doc_metadata_by_id(id: str = "wb_725385"):
    """This enpoint fetches the metadata corresponding to the given `id`.
    """

    # doc = mongodb.get_docs_metadata_collection().find_one({"id": id})
    # if doc is None:
    #     doc = mongodb.get_collection(
    #         "test_nlp", "docs_metadata").find_one({"id": id})

    doc = elasticsearch.NLPDoc.get(id=id).to_dict()

    doc = metadata.MetadataModel(**doc)

    return doc


@router.post(
    "/get_doc_count",
    # response_model=metadata.MetadataModel,
    # summary="Get count of documents based on arbitrary grouping fields.")
)
def get_doc_count(
        group_by: List[str] = ["year", "country"],
        sort_by: List[metadata.SortOn] = [
            metadata.SortOn(field="year", order=metadata.SortOrder.desc),
            metadata.SortOn(field="count", order=metadata.SortOrder.desc)],
        limit: int = 10):
    """This endpoint provides a generic interface to get the count of documents given an arbitrary set of `group_by` fields. The return value can be sorted based on the `sort_by` fields input. The number of returned groups is limited by the `limit` parameter.
    """

    assert len(set(so.field
                   for so in sort_by).difference(group_by + ['count'])) == 0

    group_id = {b: f"${b}" for b in group_by}

    sort_by = SON(
        [(so.field, -1 if so.order == metadata.SortOrder.desc else 1) for so in sort_by])
    projection = {b: f"$_id.{b}" for b in group_by}
    projection["count"] = "$count"
    projection["_id"] = 0

    # Identify fields that needs unwinding, if any
    list_fields = set(["adm_region", "author", "country", "der_acronyms", "doc_type",
                       "geo_region", "major_doc_type", "topics_src", "wb_subtopic_src"])
    unwind_fields = [{"$unwind": f"${b}"}
                     for b in list_fields.intersection(group_by)]

    pipeline = []

    if unwind_fields:
        pipeline = unwind_fields

    pipeline.extend([
        {"$group": {"_id": group_id, "count": {"$sum": 1}}},
        {"$project": projection},
        {"$sort": sort_by},
        {"$limit": limit},
    ])

    agg = mongodb.get_docs_metadata_collection().aggregate(
        pipeline
    )

    values = [{"rank": ix, **result} for ix, result in enumerate(agg, 1)]

    return values


@router.post(
    "/get_normalized_doc_count",
    # response_model=metadata.MetadataModel,
    # summary="Get count of documents based on arbitrary grouping fields.")
)
def get_normalized_doc_count(
        group_by: List[str] = ["year", "country"],
        sort_by: List[metadata.SortOn] = [
            metadata.SortOn(field="year", order=metadata.SortOrder.desc),
            metadata.SortOn(field="count", order=metadata.SortOrder.desc)],
        normalize_by: str = "year",
        limit: int = 10):
    """This endpoint provides a generic interface to get the count of documents and normalized values given an arbitrary set of `group_by` fields and a `normalize_by` field to normalize the counts with. The return value can be sorted based on the `sort_by` fields input. The number of returned groups is limited by the `limit` parameter.
    """

    assert len(set(so.field
                   for so in sort_by).difference(group_by + ['count'])) == 0

    group_id = {b: f"${b}" for b in group_by}

    sort_by = SON(
        [(so.field, -1 if so.order == metadata.SortOrder.desc else 1) for so in sort_by])

    projection = {b: f"$results._id.{b}" for b in group_by}
    projection["count"] = "$results.count"
    projection["proportion"] = "$results.proportion"
    projection["_id"] = 0

    # Identify fields that needs unwinding, if any
    list_fields = set(["adm_region", "author", "country", "der_acronyms", "doc_type",
                       "geo_region", "major_doc_type", "topics_src", "wb_subtopic_src"])
    unwind_fields = [{"$unwind": f"${b}"}
                     for b in list_fields.intersection(group_by)]

    pipeline = []

    if unwind_fields:
        pipeline = unwind_fields

    pipeline.extend([
        {"$group": {"_id": group_id, "count": {"$sum": 1}}},
        {"$group": {"_id": f"$_id.{normalize_by}",
                    "group_sum": {"$sum": "$count"},
                    "results": {"$push": "$$ROOT"}}},
        {"$project": {
            "_id": 0,
            "results": {
                "$map": {
                    "input": "$results",
                    "as": "r",
                    "in": {
                        "_id": "$$r._id",
                        "count": "$$r.count",
                        "proportion": {
                            "$divide": ["$$r.count", "$group_sum"]
                        }
                    }
                }
            }
        }},
        {"$unwind": "$results"},
        {"$project": projection},
        {"$sort": sort_by},
        {"$limit": limit},
    ])

    agg = mongodb.get_docs_metadata_collection().aggregate(
        pipeline
    )

    values = [{"rank": ix, **result} for ix, result in enumerate(agg, 1)]

    return values

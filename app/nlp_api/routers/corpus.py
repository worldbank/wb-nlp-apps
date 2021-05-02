'''This router contains the implementation for the cleaning API.
'''
from bson.son import SON
import enum
from datetime import datetime
from typing import Optional, List
from functools import lru_cache
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Body, Query

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


def get_agg_data_payload(df, field, type="line", is_share=False):
    x = sorted(df.index)
    legend = sorted(df.columns)
    series = [dict(name=f, data=(100 * df.loc[x, f]).round(2).tolist() if is_share else df.loc[x, f].round(2).tolist(),
                   stack=field, type=type, areaStyle={}) for f in legend]
    return dict(
        year=x,
        series=series,
        legend=legend,
    )


def get_agg_data_by_field(field, type="line"):
    # Get total docs per corpus by year
    # Get percent of docs per corpus by year
    #
    agg = elasticsearch.NLPDocAggregations()

    data = pd.DataFrame(agg.get_doc_counts_by_year_by_field(field=field))

    year_field_doc_count_df = data.pivot(
        index="year", columns=field, values=f"{field}_doc_count").fillna(0)
    year_doc_count_df = data.pivot(
        index="year", columns=field, values="year_doc_count").fillna(0)

    year_field_total_tokens_df = data.pivot(
        index="year", columns=field, values=f"{field}_total_tokens").fillna(0)
    year_total_tokens_df = data.pivot(
        index="year", columns=field, values="year_total_tokens").fillna(0)

    normed_year_field_doc_count_df = (
        year_field_doc_count_df / year_doc_count_df).fillna(0)

    normed_year_field_total_tokens_df = (
        year_field_total_tokens_df / year_total_tokens_df).fillna(0)

    doc_count_volume = get_agg_data_payload(
        year_field_doc_count_df, field=field, type=type)
    doc_count_share = get_agg_data_payload(
        normed_year_field_doc_count_df, field=field, type=type, is_share=True)

    total_tokens_volume = get_agg_data_payload(
        year_field_total_tokens_df, field=field, type=type)
    total_tokens_share = get_agg_data_payload(
        normed_year_field_total_tokens_df, field=field, type=type, is_share=True)

    return dict(
        field=field,
        docs=dict(
            volume=doc_count_volume,
            share=doc_count_share,
        ),
        tokens=dict(
            volume=total_tokens_volume,
            share=total_tokens_share
        )
    )


@router.get("/get_corpus_volume_by_source")
def get_corpus_volume_by_source():
    """
    This endpoint generates an aggregated data of the volume of documents and tokens present in the corpus grouped by source and year.
    """

    return get_agg_data_by_field(field="corpus")


@router.get("/get_corpus_volume_by")
def get_corpus_volume_by(fields: List[metadata.CategoricalFields] = Query(...)):
    """
    This endpoint generates an aggregated data of the volume of documents and tokens present in the corpus grouped by source and year.
    """
    payload = {}

    for k in fields:
        payload[k] = get_agg_data_by_field(field=k.value)

    return payload


# @router.get("/get_corpus_volumes")
# def get_corpus_volumes():
#     """
#     This endpoint generates an aggregated data of the volume of documents and tokens present in the corpus grouped by source and year.
#     """
#     payload = {}
#     for k in metadata.CategoricalFields:
#         payload[k] = get_agg_data_by_field(field=k.value)

#     return payload

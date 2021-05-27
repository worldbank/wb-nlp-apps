'''This router contains the implementation for the cleaning API.
'''
from functools import lru_cache
import json
from datetime import datetime
from collections import Counter
from contexttimer import Timer

from fastapi import Query, UploadFile, File, Form
from pydantic import HttpUrl

from wb_nlp.types.models import (
    ModelTypes,
    TopicCompositionParams, PartitionTopicShareParams, FullTopicProfilesParams
)
from wb_nlp.extraction import country_extractor
from wb_nlp.interfaces import mongodb, elasticsearch
from ...common.utils import (
    get_validated_model, read_uploaded_file,
    read_url_file, clean_text
)

# router = APIRouter(
#     prefix="/lda",
#     tags=["LDA Model"],
#     dependencies=[],
#     responses={404: {"description": "Not found"}},
# )

# LDA_MODEL_NAME = ModelTypes("lda")


DEFAULT_QUERY_FIELDS = dict(
    model_id=Query(..., description="Model id"),
    topn_words=Query(
        10, description="The number of top words that will be returned for each topic."),
    total_word_score=Query(
        None, description="This will return the words representing the topic with at least `total_word_score` of cumulative score (order from largest value.)"),
    topic_id=Query(..., description="Topic id of interest."),
    text=Query(..., description="Input text for topic inference."),
    topn_topics=Query(
        10, description="The number of topics that will be returned."),
    total_topic_score=Query(
        None, description="This will return the topics representing the text with at least `total_topic_score` of cumulative score (order from largest value.)"),

    year_start=Query(
        1950, description="Start of the year to return data for."),
    year_end=Query(
        datetime.now().year, description="End of the year to return data for."),
    return_records=Query(
        True, description="A flag indicating how the returned data is structured."),
    app_tag_jdc=Query(
        False, description="Tag to only return documents under the JDC collection."),
    type=Query(
        "line", description="Type of chart."
    )

)


@lru_cache(maxsize=16)
def get_model_topic_words(
    model_name: str,
    model_id: str,
    topn_words: int,
    total_word_score: float,
):
    model = get_validated_model(model_name, model_id)

    return model.get_model_topic_words(
        topn_words=topn_words,
        total_word_score=total_word_score)


def get_model_topic_ranges(
    model_name: str,
    model_id: str,
):
    model = get_validated_model(model_name, model_id)

    return model.get_topic_composition_ranges()


def get_topic_words(
    model_name: str,
    model_id: str,
    topic_id: int,
    topn_words: int,
    total_word_score: float,
):

    model = get_validated_model(model_name, model_id)

    return model.get_topic_words(
        topic_id=topic_id,
        topn_words=topn_words,
        total_word_score=total_word_score)


def get_doc_topic_words(
    model_name: str,
    model_id: str,
    text: str,
    topn_topics: int,
    topn_words: int,
    total_topic_score: float,
    total_word_score: float
):

    model = get_validated_model(model_name, model_id)

    return model.get_doc_topic_words(
        text=text,
        topn_topics=topn_topics,
        topn_words=topn_words,
        total_topic_score=total_topic_score,
        total_word_score=total_word_score)


def get_docs_by_topic_composition(
    model_name: str,
    transform_params: TopicCompositionParams
):
    model = get_validated_model(model_name, transform_params.model_id)

    topic_percentage = {
        int(k.split("_")[1]): v for k, v in transform_params.topic_percentage.items()}

    from_result = transform_params.from_result
    size = transform_params.size
    result = model.get_docs_by_topic_composition(
        topic_percentage=topic_percentage,
        from_result=from_result,
        size=size,
        return_all_topics=transform_params.return_all_topics)

    id_rank = {res["id"]: res["rank"] for res in result["hits"]}

    docs_metadata = mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = mongodb.get_docs_metadata_collection()

    response = docs_metadata.find({"id": {"$in": list(id_rank.keys())}})

    total = dict(
        value=result["total"],
        message="many"
    )

    return dict(
        total=total,
        hits=[h for h in sorted(response, key=lambda x: id_rank[x["id"]])],
        api_result=result,
        next=from_result + size,
        result=result,
    )


def get_docs_by_topic_composition_count(
    model_name: str,
    transform_params: TopicCompositionParams
):
    model = get_validated_model(model_name, transform_params.model_id)

    topic_percentage = {
        int(k.split("_")[1]): v for k, v in transform_params.topic_percentage.items()}

    return dict(total=model.get_docs_by_topic_composition_count(topic_percentage=topic_percentage))


def get_partition_topic_share(
    model_name: str,
    transform_params: PartitionTopicShareParams
):
    model = get_validated_model(model_name, transform_params.model_id)

    transform_params = json.loads(transform_params.json())
    transform_params.pop("model_id")

    return model.get_partition_topic_share(**transform_params)


def get_full_topic_profiles(
    model_name: str,
    model_id: str,
    topic_id: int,
    year_start: int,
    year_end: int,
    return_records: bool,
    app_tag_jdc: bool,
    type: str
):
    model = get_validated_model(model_name, model_id)

    filters = None
    if app_tag_jdc:
        filters = [{"term": {"app_tag_jdc": app_tag_jdc}}]

    return model.get_full_topic_profiles(
        topic_id=topic_id,
        year_start=year_start,
        year_end=year_end,
        return_records=return_records,
        filters=filters,
        type=type,
    )


def get_topics_by_doc_id(
    model_name: ModelTypes,
    model_id: str,
    doc_id: str,
    topn_words: int,
    total_word_score: float,
    sort: bool,
    format_words: bool
):
    with Timer() as timer:
        print(f"E1: {timer.elapsed}")

        topic_words = get_model_topic_words(
            model_name=model_name,
            model_id=model_id,
            topn_words=topn_words,
            total_word_score=total_word_score,
        )
        print(f"E2: {timer.elapsed}")
        topic_words = {topic["topic_id"]: topic["topic_words"]
                       for topic in topic_words}

        print(f"E3: {timer.elapsed}")

        # doc_topic_data = mongodb.get_document_topics_collection().find_one(
        #     {"model_run_info_id": model_id, "id": doc_id})

        doc_topic_data = elasticsearch.DocTopic.get(
            id=f"{model_id}-{doc_id}").to_dict()

        print(f"E4: {timer.elapsed}")

        payload = []

        items = doc_topic_data["topics"].items()
        if sort:
            items = sorted(items, key=lambda x: -x[1])

        for topic_id_str, value in items:
            topic_id = int(topic_id_str.split("_")[-1])
            payload.append(
                dict(
                    topic_id=topic_id,
                    topic_words=topic_words[topic_id] if not format_words else ", ".join(
                        [i["word"] for i in topic_words[topic_id]]),
                    value=value
                )
            )
        print(f"E5: {timer.elapsed}")

        return payload


def analyze_document(
    model_name: ModelTypes,
    model_id: str,
    text: str,
    topn_words: int = 10,
    total_word_score: float = 1,
    sort: bool = True,
    clean: bool = True,
    format_words: bool = True
):
    # Get country related metadata

    country_counts = country_extractor.get_country_counts(text)
    country_details = country_extractor.get_country_count_details(
        country_counts)

    country_groups = []
    if country_details is not None:
        for cd in country_details:
            code = cd.get("code")
            if code:
                g = country_extractor.country_code_country_group_map.get(code)
                if g:
                    country_groups.extend(g)

    model = get_validated_model(model_name, model_id)

    if clean:
        model_text = clean_text(model_name, model_id, text)
        # query = model.clean_text(query)
    else:
        model_text = text

    topic_words = model.get_doc_topic_words(
        text=model_text,
        topn_topics=10,
        topn_words=topn_words,
        total_topic_score=1,
        total_word_score=total_word_score,
        serialize=False)

    if sort:
        topic_words = sorted(topic_words, key=lambda x: -x["score"])

    doc_topic_words = [
        dict(
            topic_id=topic_word["topic"],
            topic_words=", ".join(
                [w["word"] for w in topic_word["words"]]) if format_words else topic_word["words"],
            value=topic_word["score"]) for topic_word in topic_words]

    return dict(
        doc_topic_words=doc_topic_words,
        country_counts=country_counts,
        country_details=country_details,
        country_groups=dict(Counter(country_groups).most_common()),
    )


def analyze_file(
    model_name: ModelTypes,
    model_id: str = Form(...),
    file: UploadFile = File(...),
    topn_words: int = Form(10),
    total_word_score: float = Form(1.0),
    sort: bool = Form(True),
    clean: bool = Form(True),
    format_words: bool = Form(True)

):
    '''This endpoint provides the service for analyzing uploaded file. This returns extracted countries from the document and the infered topics based on the model selected.
    '''
    print({"filename": file.filename})

    document = read_uploaded_file(file)

    return analyze_document(
        model_name=model_name,
        model_id=model_id,
        text=document,
        topn_words=topn_words,
        total_word_score=total_word_score,
        sort=sort,
        clean=clean,
        format_words=format_words,)


def analyze_url(
    model_name: ModelTypes,
    model_id: str = Form(...),
    url: HttpUrl = Form(...),
    topn_words: int = Form(10),
    total_word_score: float = Form(1.0),
    sort: bool = Form(True),
    clean: bool = Form(True),
    format_words: bool = Form(True)

):
    '''This endpoint provides the service for analyzing a document given a url. This returns extracted countries from the document and the infered topics based on the model selected.
    '''

    document = read_url_file(url)

    return analyze_document(
        model_name=model_name,
        model_id=model_id,
        text=document,
        topn_words=topn_words,
        total_word_score=total_word_score,
        sort=sort,
        clean=clean,
        format_words=format_words,)

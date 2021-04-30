'''This router contains the implementation for the cleaning API.
'''

from fastapi import APIRouter, Query

from wb_nlp.types.models import (
    ModelTypes, MetricTypes
)

from ...common.utils import get_validated_model

router = APIRouter(
    prefix="/word2vec",
    tags=["Word2vec Model"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ router.get("/get_similar_words_graph")
async def get_similar_words_graph(
    model_id: str = Query(..., description="Identification of the desired model configuration to use for the operation. The cleaning pipeline associated with this model will also be applied."),
    raw_text: str = Query(
        ..., description="Input text to transform."),
    topn_words: int = Query(
        10, ge=1, description='Number of similar words to return.'),
    metric: MetricTypes = Query(MetricTypes.cosine_similarity),
    topn_sub: int = Query(
        5, ge=1, description='Number of similar words to primary related words.'),
    edge_thresh: float = Query(
        0.5, description="Minimum similarity score."
    ),
        n_clusters: int = Query(5, description="Number of clusters.")):
    '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
    '''
    model = get_validated_model(ModelTypes(
        "word2vec"), model_id)

    return model.get_similar_words_graph(
        document=raw_text,
        topn=topn_words,
        topn_sub=topn_sub,
        edge_thresh=edge_thresh,
        n_clusters=n_clusters,
        metric=metric.value)

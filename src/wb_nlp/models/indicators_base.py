import logging
from hashlib import md5

import pandas as pd
from milvus import DataType
from wb_nlp.interfaces.milvus import (
    get_milvus_client,
    get_collection_ids,
    get_embedding_dsl,
    get_hex_id,
    get_int_id,
)
from wb_nlp import dir_manager
from wb_nlp.models import word2vec_base


class IndicatorModel:
    def __init__(self, data_file, indicator_code, model_config_id, cleaning_config_id, model_run_info_id, log_level=logging.WARNING):
        """
        Input
        =====
        data_file = File of the metadata for the indicator containing the text to be embedded.
        indicator_code = Slug name/code for the indicator, e.g., wdi, sdg, timeseries-meta, etc.
        """
        self.data_file = data_file
        self.model_config_id = model_config_id
        self.cleaning_config_id = cleaning_config_id
        self.model_run_info_id = model_run_info_id
        self.log_level = log_level
        self.indicator_code = indicator_code

        self.model_collection_id = f"indicator_{model_run_info_id}_{indicator_code}"

        self.wvec_model = self.load_wvec_model()
        self.load_metadata_file()

    def load_metadata_file(self):
        indicator_df = pd.read_csv(self.data_file)

        indicator_df["hex_id"] = indicator_df['id'].map(
            lambda x: md5(x.encode('utf-8')).hexdigest()[:15])
        indicator_df["int_id"] = indicator_df["hex_id"].map(
            lambda x: int(x, 16))

        self.indicator_df = indicator_df

    def generate_vectors(self):
        milvus_client = get_milvus_client()
        collection_name = self.model_collection_id

        docs_metadata_df = self.indicator_df

        if collection_name not in milvus_client.list_collections():
            milvus_client.create_collection(
                collection_name, self.collection_params)

        collection_doc_ids = set(get_collection_ids(collection_name))

        docs_for_processing = docs_metadata_df[
            ~docs_metadata_df['int_id'].isin(collection_doc_ids)]

        docs_for_processing["text"] = docs_for_processing["txt_meta"].map(
            self.wvec_model.clean_text)

        results = self.wvec_model.process_docs(
            docs_for_processing, normalize=True)
        results = [(ix, p['doc_vec'].flatten())
                   for ix, (_, p) in enumerate(results.iterrows()) if p['success']]

        locs, vectors = list(zip(*results))

        doc_int_ids = docs_for_processing.iloc[list(
            locs)]['int_id'].tolist()
        doc_ids = docs_for_processing.iloc[list(
            locs)]['id'].tolist()

        entities = [
            {"name": self.milvus_vector_field_name, "values": vectors,
                "type": DataType.FLOAT_VECTOR},
        ]

        if not milvus_client.has_partition(collection_name, self.indicator_code):
            milvus_client.create_partition(
                collection_name, self.indicator_code)

        ids = milvus_client.insert(collection_name, entities,
                                   doc_int_ids, partition_tag=self.indicator_code)

        assert len(set(ids).difference(
            doc_int_ids)) == 0

        milvus_client.flush([collection_name])

    def load_wvec_model(self):
        self.wvec_model = word2vec_base.Word2VecModel(
            model_config_id=self.model_config_id,
            cleaning_config_id=self.cleaning_config_id,
            model_run_info_id=self.model_run_info_id,
            raise_empty_doc_status=False,
            log_level=self.log_level,
        )

        return self.wvec_model

    def get_similar_indicators_by_doc_id(self, doc_id):
        avec = self.wvec_model.get_milvus_doc_vector_by_doc_id(
            doc_id).reshape(1, -1)
        pass

    def get_similar_indicators_by_vector(self, vector):
        pass

    def create_milvus_collection(self):
        self.milvus_vector_field_name = "embedding"

        self.collection_params = {
            "fields": [
                {"name": self.milvus_vector_field_name, "type": DataType.FLOAT_VECTOR,
                    "params": {"dim": self.wvec_model.dim}},
            ],
            "segment_row_limit": 4096,
            "auto_id": False
        }

        if self.model_collection_id not in get_milvus_client().list_collections():
            get_milvus_client().create_collection(
                self.model_collection_id, self.collection_params)

    def drop_milvus_collection(self):
        if self.model_collection_id in get_milvus_client().list_collections():
            get_milvus_client().drop_collection(self.model_collection_id)


if __name__ == "__main__":
    from wb_nlp.models import indicators_base
    from wb_nlp import dir_manager

    model = indicators_base.IndicatorModel(
        data_file=dir_manager.get_data_dir(
            "preprocessed", "timeseries", "wdi_time_series_metadata.csv"),
        indicator_code="wdi",
        model_config_id="702984027cfedde344961b8b9461bfd3",
        cleaning_config_id="229abf370f281efa7c9f3c4ddc20159d",
        model_run_info_id="0d63e5ae71e4f78fc427ddbec2fefc73",
        log_level=logging.DEBUG)


# wdi_df = pd.read_csv(dir_manager.get_data_dir(
#     "preprocessed", "timeseries", "wdi_time_series_metadata.csv"))

# wdi_df["text"] = wdi_df["txt_meta"].map(wvec_model.clean_text)

# wdi_df["vector"] = wdi_df.apply(
#     lambda x: wvec_model.process_doc(x)["doc_vec"], axis=1)

# wdi_df.to_pickle(
#     f"/workspace/models/wdi/wdi_time_series_metadata-{wvec_model.model_id}.pickle")

# wvec_model.drop_milvus_collection()


# @ router.get("/get_similar_wdi_by_doc_id")
# async def get_similar_wdi_by_doc_id(doc_id: str, model_id: str, topn: int = 10):
#     '''This endpoint converts the `raw_text` provided into a vector transformed using the specified word2vec model.
#     '''
#     model = get_validated_model(ModelTypes(
#         "word2vec"), model_id)

#     avec = model.get_milvus_doc_vector_by_doc_id(doc_id).reshape(1, -1)
#     wdi_df = pd.read_pickle(dir_manager.get_path_from_root(
#         "models", "wdi", f"wdi_time_series_metadata-{model.model_id}.pickle"))

#     vecs = np.vstack(wdi_df["vector"].values)
#     sim = cosine_similarity(avec, vecs)[0]
#     sorted_idx = sim.argsort()[::-1]

#     wdi_df["score"] = sim
#     wdi_df = wdi_df.iloc[sorted_idx]

#     ret_cols = ["id", "name", "url_data", "url_meta", "url_wb", "score"]

#     return wdi_df[ret_cols].head(topn).to_dict("records")

import pandas as pd
from wb_nlp import dir_manager
from wb_nlp.models import word2vec_base

wvec_model = word2vec_base.Word2VecModel(
    # "702984027cfedde344961b8b9461bfd3",
    model_config_id="702984027cfedde344961b8b9461bfd3",
    # "23f78350192d924e4a8f75278aca0e1c",
    cleaning_config_id="229abf370f281efa7c9f3c4ddc20159d",
    raise_empty_doc_status=False,
    log_level=None,
)

wdi_df = pd.read_csv(dir_manager.get_data_dir(
    "preprocessed", "timeseries", "wdi_time_series_metadata.csv"))

wdi_df["text"] = wdi_df["txt_meta"].map(wvec_model.clean_text)

wdi_df["vector"] = wdi_df.apply(
    lambda x: wvec_model.process_doc(x)["doc_vec"], axis=1)

wdi_df.to_pickle(
    f"/workspace/models/wdi/wdi_time_series_metadata-{wvec_model.model_id}.pickle")

# wvec_model.drop_milvus_collection()

import logging

from wb_nlp.models.indicators_base import IndicatorModel
from wb_nlp import dir_manager


class SDGModel(IndicatorModel):
    def __init__(
            self,
            data_file=dir_manager.get_data_dir(
                "preprocessed", "timeseries", "sdg", "sdg_time_series_metadata_merged_data.csv"),
            indicator_code="sdg",
            model_config_id=None, cleaning_config_id=None,
            model_run_info_id=None, log_level=logging.WARNING):
        super().__init__(
            data_file=data_file,
            indicator_code=indicator_code,
            model_config_id=model_config_id,
            cleaning_config_id=cleaning_config_id,
            model_run_info_id=model_run_info_id,
            log_level=log_level,
        )


# model = indicators_base.IndicatorModel(
#     data_file=dir_manager.get_data_dir(
#         "preprocessed", "timeseries", "wdi_time_series_metadata.csv"),
#     indicator_code="wdi",
#     model_config_id="702984027cfedde344961b8b9461bfd3",
#     cleaning_config_id="229abf370f281efa7c9f3c4ddc20159d",
#     model_run_info_id="0d63e5ae71e4f78fc427ddbec2fefc73",
#     log_level=logging.INFO)

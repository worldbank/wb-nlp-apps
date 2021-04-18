from wb_nlp.models.indicators_base import IndicatorModel
from wb_nlp import dir_manager
import logging


class WDIModel(IndicatorModel):
    pass


# model = indicators_base.IndicatorModel(
#     data_file=dir_manager.get_data_dir(
#         "preprocessed", "timeseries", "wdi_time_series_metadata.csv"),
#     indicator_code="wdi",
#     model_config_id="702984027cfedde344961b8b9461bfd3",
#     cleaning_config_id="229abf370f281efa7c9f3c4ddc20159d",
#     model_run_info_id="0d63e5ae71e4f78fc427ddbec2fefc73",
#     log_level=logging.INFO)

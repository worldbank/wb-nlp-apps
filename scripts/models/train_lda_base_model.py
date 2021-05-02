#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import click
import wb_nlp
from wb_nlp.models import lda_base


# fallback to debugger on error

_logger = logging.getLogger(__name__)


@click.command()
@click.option('-mcid', '--model-config-id', 'model_config_id', required=True,
              help='Configuration id for the configuration of the model that will be used.')
@click.option('-ccid', '--cleaning-config-id', 'cleaning_config_id', required=True,
              help='Configuration id of the cleaning pipeline used in cleaning the input data.')
@click.option('-desc', '--description', 'description', required=True,
              help='Short description of the model run.')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(model_config_id: str, cleaning_config_id: str, description: str, log_level: int):

    print(model_config_id, cleaning_config_id, description, log_level)

    lda_model = lda_base.LDAModel(
        model_config_id=model_config_id,  # "ef0ab0459e9c28de8657f3c4f5b2cd86",
        cleaning_config_id=cleaning_config_id,  # "23f78350192d924e4a8f75278aca0e1c",
        raise_empty_doc_status=False,
        model_run_info_description=description,
        log_level=log_level,  # logging.DEBUG,
    )

    lda_model.train_model(retrain=True)


if __name__ == '__main__':
    # python -u ./scripts/models/train_lda_base_model.py --model-config-id <model_config_id> --cleaning-config-id <cleaning_config_id> --description <description> -vv |& tee ./data/logs/train_lda_base_model.py.log
    # python -u ./scripts/models/train_lda_base_model.py --model-config-id ef0ab0459e9c28de8657f3c4f5b2cd86 --cleaning-config-id 23f78350192d924e4a8f75278aca0e1c --description lda_model -vv |& tee ./data/logs/train_lda_base_model.py.log
    main()

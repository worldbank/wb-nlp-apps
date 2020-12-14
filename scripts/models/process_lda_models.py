#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script generates excel files containing a summary of topics for each available model.
'''

import logging
from pathlib import Path
import json
import click
import pandas as pd

from gensim.models.ldamodel import LdaModel

# from joblib import Parallel, delayed
# import joblib

import wb_nlp
from wb_nlp.utils.scripts import configure_logger


_logger = logging.getLogger(__file__)


def checkpoint_log(timer, logger, message=''):
    logger.info('Time elapsed now in minutes: %s %s',
                timer.elapsed / 60, message)


@click.command()
@click.option('--model-base-dir', 'model_base_dir', required=True,
              type=click.Path(exists=True), help='path to root directory of the LDA models')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(model_base_dir: Path, log_level: int):
    '''
    Entry point for LDA model training script.
    '''
    model_base_dir = Path(model_base_dir)

    configure_logger(log_level)

    with pd.ExcelWriter(
            model_base_dir / 'lda_model_topic_words.xlsx', engine='xlsxwriter') as writer:

        # Discover available models:
        for model_dir in model_base_dir.glob('*'):
            if not model_dir.is_dir():
                continue

            _logger.info('Processing model_dir: %s', model_dir)

            confs = [conf for conf in model_dir.glob(
                'model_config_*.json')]
            assert len(confs) <= 1

            if len(confs) == 0:
                continue

            conf = confs[0]
            with open(conf) as json_file:
                config = json.load(json_file)

            model_id = str(conf).split('_')[-1].split('.')[0]

            model_path = model_dir / f'model_{model_id}.lda.bz2'
            if not model_path.exists():
                continue

            lda = LdaModel.load(str(model_path))

            topic_id_words = {}

            for topic_id, topic_words in lda.print_topics(num_topics=-1, num_words=20):
                _, words = zip(*list(
                    map(lambda x: x.split('*'), topic_words.split(' + '))))

                words = {f'word_{str(wn).zfill(2)}': w for wn, w in enumerate(
                    map(lambda x: x.strip('"'), words))}

                topic_id = f"topic_{str(topic_id).zfill(2)}"

                topic_id_words[topic_id] = words

            topic_id_words = pd.DataFrame(topic_id_words).T
            lda_config = config['params']['lda']
            sheet_name = f"{model_id[:4]}-dim={lda_config['num_topics']}-passes={lda_config['passes']}-iter={lda_config['iterations']}"

            topic_id_words.to_excel(writer, sheet_name=sheet_name)


if __name__ == '__main__':
    # Use in local machine
    # python -u scripts/models/process_lda_models.py --model-base-dir models/lda -vv |& tee ./logs/process_lda_models.py.log

    # Use in w1lxbdatad07
    # python -u scripts/models/process_lda_models.py --model-base-dir /data/wb536061/wb_nlp/models/lda -vv |& tee ./logs/process_lda_models.py.log

    main()

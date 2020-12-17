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
import numpy as np
from gensim.models.wrappers import LdaMallet
import seaborn as sns
# from joblib import Parallel, delayed
# import joblib

import wb_nlp
from wb_nlp.utils.scripts import configure_logger


_logger = logging.getLogger(__file__)

cm = sns.light_palette('green', as_cmap=True)


def get_colors(v):
    '''Transform a value to a style color.
    '''
    r, g, b, a = cm(v)
    r, g, b = list(map(int, 255 * np.array([r, g, b])))
    color = '#000000'
    if r + g + b < 200:
        color = '#ffffff'

    return f'background-color: #{r:02x}{g:02x}{b:02x}; color: {color};'


# def apply_color(x, df2):
#     colors = {1: 'green', 2: 'blue', 3: 'yellow', 4: 'orange', 5: 'grey'}
#     return df2.applymap(lambda val: get_colors(val))

# df1.style.apply(lambda x: df2.applymap(lambda val: get_colors(val)), axis=None)


@click.command()
@click.option('--model-base-dir', 'model_base_dir', required=True,
              type=click.Path(exists=True), help='path to root directory of the Mallet models')
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
            model_base_dir / 'mallet_model_topic_words.xlsx', engine='xlsxwriter') as writer:

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

            model_path = model_dir / f'model_{model_id}.mallet.bz2'
            if not model_path.exists():
                continue

            mallet = LdaMallet.load(str(model_path))

            topic_id_words = {}
            topic_id_scores = {}

            for topic_id, topic_words in mallet.print_topics(num_topics=-1, num_words=20):
                scores, words = zip(*list(
                    map(lambda x: x.split('*'), topic_words.split(' + '))))

                words = {f'word_{str(wn).zfill(2)}': w for wn, w in enumerate(
                    map(lambda x: x.strip('"'), words))}

                scores = {f'word_{str(wn).zfill(2)}': s for wn,
                          s in enumerate(map(float, scores))}

                topic_id = f"topic_{str(topic_id).zfill(2)}"

                topic_id_words[topic_id] = words
                topic_id_scores[topic_id] = scores

            topic_id_words = pd.DataFrame(topic_id_words).T
            topic_id_scores = pd.DataFrame(topic_id_scores).T

            topic_id_words_styled = topic_id_words.style.apply(
                lambda x: (topic_id_scores / topic_id_scores.max().max()).applymap(get_colors), axis=None)

            print(topic_id_words_styled)

            mallet_config = config['params']['mallet']
            sheet_name = f"{model_id[:4]}-dim={mallet_config['num_topics']}-alpha={mallet_config['alpha']}-iter={mallet_config['iterations']}"

            topic_id_words_styled.to_excel(writer, sheet_name=sheet_name)


if __name__ == '__main__':
    # Use in local machine
    # python -u scripts/models/process_mallet_models.py --model-base-dir models/mallet -vv |& tee ./logs/process_mallet_models.py.log

    # Use in w1lxbdatad07
    # python -u scripts/models/process_mallet_models.py --model-base-dir /data/wb536061/wb_nlp/models/mallet -vv |& tee ./logs/process_mallet_models.py.log

    main()

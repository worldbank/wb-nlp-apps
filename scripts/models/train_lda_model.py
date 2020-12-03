#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script runs the LDA model training.
'''

import logging
from pathlib import Path
import os
import itertools
import json
import click
import gensim

from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore

# from joblib import Parallel, delayed
# import joblib

import wb_nlp
from wb_nlp import dir_manager
from wb_nlp.utils.scripts import (
    configure_logger,
    load_config, generate_model_hash,
    generate_files, create_get_directory,
    create_dask_cluster,
)


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--config', 'cfg_path', required=True,
              type=click.Path(exists=True), help='path to config file')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(cfg_path: Path, log_level: int):
    '''
    Entry point for LDA model training script.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    # est = wb_nlp.models.Estimator()

    config = load_config(cfg_path, 'model_config', _logger)

    assert gensim.__version__ == config['meta']['library_version']

    input_dir = Path(dir_manager.get_path_from_root(
        config['paths']['input_dir']))
    model_dir = Path(dir_manager.get_path_from_root(
        config['paths']['model_dir']))

    if not model_dir.exists():
        model_dir.mkdir(parents=True)

    client = create_dask_cluster(_logger)
    _logger.info(client)

    _logger.info('Training dictionary...')
    dictionary_params = config['params']['dictionary']
    g_dict = Dictionary(generate_files(input_dir, split=True))
    g_dict.filter_extremes(
        no_below=dictionary_params['no_below'],
        no_above=dictionary_params['no_above'],
        keep_n=dictionary_params['keep_n'],
        keep_tokens=dictionary_params['keep_tokens'])
    g_dict.id2token = {id: token for token, id in g_dict.token2id.items()}

    _logger.info('Generating corpus...')
    corpus = [g_dict.doc2bow(d) for d in generate_files(input_dir, split=True)]

    _logger.info('Generating model configurations...')
    # Find parameters that are lists
    lda_params = config['params']['lda']
    list_params = sorted(
        filter(lambda x: isinstance(lda_params[x], list), lda_params))
    _logger.info(list_params)

    lda_params['workers'] = max(1, os.cpu_count() + lda_params['workers'])

    lda_params_set = []

    for vals in itertools.product(*[lda_params[lp] for lp in list_params]):
        _lda_params = dict(lda_params)
        for k, val in zip(list_params, vals):
            _lda_params[k] = val
        lda_params_set.append(_lda_params)

    _logger.info('Training models...')
    for model_params in lda_params_set:
        record_config = dict(config)
        record_config['params']['lda'] = dict(model_params)
        record_config['meta']['model_id'] = ''

        model_hash = generate_model_hash(record_config)
        sub_model_dir = create_get_directory(model_dir, model_hash)

        _logger.info(model_params)
        model_params['id2word'] = dict(g_dict.id2token)

        lda = LdaMulticore(corpus, **model_params)

        # TODO: Find a better strategy to name models.
        # It can be a hash of the config values for easier tracking?
        lda.save(str(sub_model_dir / f'model_{model_hash}.lda.bz2'))

        with open(sub_model_dir / 'model_config.json', 'w') as open_file:
            json.dump(record_config, open_file)

        _logger.info(lda.print_topics())
        # lda.update(corpus)
        break


if __name__ == '__main__':
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/default.yml -vv |& tee train_lda_model.py.log
    main()

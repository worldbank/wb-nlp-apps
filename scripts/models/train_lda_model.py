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

from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore

# from joblib import Parallel, delayed
# import joblib

import wb_nlp
from wb_nlp import dir_manager
from wb_nlp.utils.scripts import (
    configure_logger,
    load_config, generate_model_hash,
    create_get_directory
)

from wb_nlp.processing.corpus import MultiDirGenerator


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--config', 'cfg_path', required=True,
              type=click.Path(exists=True), help='path to config file')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--train-dictionary', 'load_dictionary', flag_value=False, default=True)
@click.option('--load-dictionary', 'load_dictionary', flag_value=True)
@click.option('--from-files', 'load_dump', flag_value=False, default=True)
@click.option('--from-dump', 'load_dump', flag_value=True)
@click.version_option(wb_nlp.__version__)
def main(cfg_path: Path, log_level: int, load_dictionary: bool, load_dump: bool):
    '''
    Entry point for LDA model training script.
    '''
    configure_logger(log_level)

    if load_dump:
        assert load_dictionary, "Can't load a corpus dump without using the --load-dictionary flag."

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    # est = wb_nlp.models.Estimator()

    config = load_config(cfg_path, 'model_config', _logger)

    assert gensim.__version__ == config['meta']['library_version']

    paths_conf = config['paths']

    model_dir = Path(dir_manager.get_path_from_root(paths_conf['model_dir']))
    if not model_dir.exists():
        model_dir.mkdir(parents=True)

    corpus_path = paths_conf['corpus_path']
    file_generator = MultiDirGenerator(
        base_dir=paths_conf['base_dir'],
        source_dir_name=paths_conf['source_dir_name'],
        split=True,
        min_tokens=config['params']['min_tokens']
    )

    _logger.info('Training dictionary...')
    dictionary_params = config['params']['dictionary']
    # dictionary_hash = generate_model_hash(dictionary_params)

    dictionary_file = Path(paths_conf['dictionary_path'])

    if load_dictionary and dictionary_file.exists():
        g_dict = Dictionary.load(str(dictionary_file))
    else:
        assert not load_dump, "Can't generate dictionary if trying to use a corpus dump. Use --from-files flag instead."

        g_dict = Dictionary(file_generator)
        g_dict.filter_extremes(
            no_below=dictionary_params['no_below'],
            no_above=dictionary_params['no_above'],
            keep_n=dictionary_params['keep_n'],
            keep_tokens=dictionary_params['keep_tokens'])
        g_dict.id2token = {id: token for token, id in g_dict.token2id.items()}
        g_dict.save(str(dictionary_file))

    if load_dump:
        _logger.info('Loading saved corpus...')
        corpus = MmCorpus.load(corpus_path)
    else:
        _logger.info('Generating corpus...')
        corpus = [g_dict.doc2bow(d) for d in file_generator]

        _logger.info('Saving corpus to %s...', corpus_path)
        MmCorpus.serialize(corpus_path, corpus)

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

        _logger.info("Training model_id: %s", model_hash)
        _logger.info(model_params)
        model_params['id2word'] = dict(g_dict.id2token)

        lda = LdaMulticore(corpus, **model_params)

        # TODO: Find a better strategy to name models.
        # It can be a hash of the config values for easier tracking?
        lda.save(str(sub_model_dir / f'model_{model_hash}.lda.bz2'))

        with open(sub_model_dir / f'model_config_{model_hash}.json', 'w') as open_file:
            json.dump(record_config, open_file)

        _logger.info(lda.print_topics())
        # lda.update(corpus)
        # break


if __name__ == '__main__':
    # Use in local machine
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/test.yml -vv |& tee train_lda_model.py.log

    # Use in w1lxbdatad07
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/default.yml -vv |& tee train_lda_model.py.log
    main()

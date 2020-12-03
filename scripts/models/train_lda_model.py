#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import os
import sys

import click
from IPython.core import ultratb

import wb_nlp
from wb_nlp import dir_manager
from wb_nlp.configs.utils import load_config

import itertools
import gensim
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore

from dask.distributed import Client, LocalCluster, progress
from joblib import Parallel, delayed
import joblib
# # fallback to debugger on error
# sys.excepthook = ultratb.FormattedTB(
#     mode='Verbose', color_scheme='Linux', call_pdb=1)


def load_file(fname: Path, split: bool = True):
    with open(fname) as fl:
        txt = fl.read()

    return txt.split() if split else txt


def generate_files(path: Path, split: bool = True):
    return map(lambda x: load_file(x, split=split), path.glob('*.txt'))


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--config', 'cfg_path', required=True,
              type=click.Path(exists=True), help='path to config file')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(cfg_path: Path, log_level: int):
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    # est = wb_nlp.models.Estimator()

    config = load_config(cfg_path, 'model_config', _logger)

    assert(gensim.__version__ == config['meta']['library_version'])

    input_dir = Path(dir_manager.get_path_from_root(
        config['paths']['input_dir']))
    model_dir = Path(dir_manager.get_path_from_root(
        config['paths']['model_dir']))

    if not model_dir.exists():
        model_dir.mkdir(parents=True)

    # _logger.info('Creating dask client...')
    # cluster = LocalCluster(n_workers=max(1, os.cpu_count() - 4), dashboard_address=':8887',
    #                        threads_per_worker=1, processes=True, memory_limit=0)
    # client = Client(cluster)
    # _logger.info(client)
    # _logger.info(client.dashboard_link)

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
        for k, v in zip(list_params, vals):
            _lda_params[k] = v
        lda_params_set.append(_lda_params)

    _logger.info('Training models...')
    for ix, model_params in enumerate(lda_params_set):
        _logger.info(model_params)

        model_params['id2word'] = dict(g_dict.id2token)

        lda = LdaMulticore(corpus, **model_params)

        # TODO: Find a better strategy to name models.
        # It can be a hash of the config values for easier tracking?
        lda.save(os.path.join(model_dir, f'model-{ix}.lda'))
        _logger.info(lda.print_topics())
        # lda.update(corpus)
        break


if __name__ == '__main__':
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/default.yml -v
    main()

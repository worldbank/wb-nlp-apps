#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import sys

import click
from IPython.core import ultratb

import wb_nlp
from wb_nlp.configs.utils import load_config

import gensim
from gensim.models.ldamulticore import LdaMulticore

# # fallback to debugger on error
# sys.excepthook = ultratb.FormattedTB(
#     mode='Verbose', color_scheme='Linux', call_pdb=1)

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

    # Compute using gensim dictionary
    id2word = {}
    corpus = []

    # Find parameters that are lists
    params = config['params']
    list_params = sorted(filter(lambda x: isinstance(params[x], list), params))
    _logger.info(list_params)

    params['id2word'] = id2word

    params_set = []

    for lp in list_params:
        for v in params[lp]:
            pass

    lda = LdaMulticore(**params)
    lda.update(corpus)


if __name__ == '__main__':
    main()

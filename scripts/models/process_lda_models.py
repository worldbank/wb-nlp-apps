#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script generates excel files containing a summary of topics for each available model.
'''

import logging
from pathlib import Path
import os
import itertools
import json
import click
import gensim
import pandas as pd

import contexttimer
from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamodel import LdaModel

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

            confs = [conf for conf in model_dir.glob(
                'model_config_*.json')]
            assert len(confs) <= 1

            if len(confs) == 0:
                continue

            conf = confs[0]
            with open(conf) as json_file:
                config = json.load(json_file)

            model_path = model_dir / f'model_{model_id}.lda.bz2'
            if not model_path.exists():
                continue

            model_id = conf.split('_')[-1].split('.')[0]

            lda = LdaModel.load(str(model_path))

            topic_id_words = {}

            for topic_id, topic_words in lda.print_topics(num_topics=-1, num_words=20):
                _, words = list(
                    map(lambda x: x.split('*'), topic_words.split(' + ')))
                words = {f'word_{str(wn).zfill(2)}': w for wn, w in enumerate(
                    map(lambda x: x.strip('"'), words))}

                topic_id_words[topic_id] = words

            topic_id_words = pd.DataFrame(topic_id_words)
            lda_config = config['params']['lda']

            topic_id_words.to_excel(writer, sheet_name=model_id)

        # if load_dump:
        #     assert load_dictionary, "Can't load a corpus dump without using the --load-dictionary flag."

        # # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
        # # est = wb_nlp.models.Estimator()

        # config = load_config(cfg_path, 'model_config', _logger)

        # assert gensim.__version__ == config['meta']['library_version']

        # paths_conf = config['paths']

        # model_dir = Path(dir_manager.get_path_from_root(
        #     paths_conf['model_dir']))
        # if not model_dir.exists():
        #     model_dir.mkdir(parents=True)

        # corpus_path = paths_conf['corpus_path']
        # file_generator = MultiDirGenerator(
        #     base_dir=paths_conf['base_dir'],
        #     source_dir_name=paths_conf['source_dir_name'],
        #     split=True,
        #     min_tokens=config['params']['min_tokens'],
        #     logger=_logger
        # )

        # _logger.info('Training dictionary...')
        # dictionary_params = config['params']['dictionary']
        # # dictionary_hash = generate_model_hash(dictionary_params)

        # dictionary_file = Path(paths_conf['dictionary_path'])

        # checkpoint_log(
        #     timer, _logger, message='Loading or generating dictionary...')

        # if load_dictionary and dictionary_file.exists():
        #     g_dict = Dictionary.load(str(dictionary_file))
        # else:
        #     assert not load_dump, "Can't generate dictionary if trying to use a corpus dump. Use --from-files flag instead."

        #     g_dict = Dictionary(file_generator)
        #     g_dict.filter_extremes(
        #         no_below=dictionary_params['no_below'],
        #         no_above=dictionary_params['no_above'],
        #         keep_n=dictionary_params['keep_n'],
        #         keep_tokens=dictionary_params['keep_tokens'])
        #     g_dict.id2token = {id: token for token,
        #                        id in g_dict.token2id.items()}
        #     g_dict.save(str(dictionary_file))

        # checkpoint_log(
        #     timer, _logger, message='Loading or generating corpus...')

        # if load_dump:
        #     _logger.info('Loading saved corpus...')
        #     corpus = MmCorpus(corpus_path)
        # else:
        #     _logger.info('Generating corpus...')
        #     corpus = [g_dict.doc2bow(d) for d in file_generator]

        #     _logger.info('Saving corpus to %s...', corpus_path)
        #     MmCorpus.serialize(corpus_path, corpus)

        # _logger.info('Generating model configurations...')
        # # Find parameters that are lists
        # lda_params = config['params']['lda']
        # list_params = sorted(
        #     filter(lambda x: isinstance(lda_params[x], list), lda_params))
        # _logger.info(list_params)

        # lda_params['workers'] = max(1, os.cpu_count() + lda_params['workers'])

        # lda_params_set = []

        # for vals in itertools.product(*[lda_params[lp] for lp in list_params]):
        #     _lda_params = dict(lda_params)
        #     for k, val in zip(list_params, vals):
        #         _lda_params[k] = val
        #     lda_params_set.append(_lda_params)

        # _logger.info('Training models...')
        # checkpoint_log(timer, _logger, message='Starting now...')
        # models_count = len(lda_params_set)

        # for model_num, model_params in enumerate(lda_params_set, 1):
        #     record_config = dict(config)
        #     record_config['params']['lda'] = dict(model_params)
        #     record_config['meta']['model_id'] = ''

        #     model_hash = generate_model_hash(record_config)
        #     sub_model_dir = create_get_directory(model_dir, model_hash)

        #     with open(sub_model_dir / f'model_config_{model_hash}.json', 'w') as open_file:
        #         json.dump(record_config, open_file)

        #     _logger.info("Training model_id: %s", model_hash)
        #     _logger.info(model_params)
        #     model_params['id2word'] = dict(g_dict.id2token)

        #     lda = LdaMulticore(corpus, **model_params)

        #     # TODO: Find a better strategy to name models.
        #     # It can be a hash of the config values for easier tracking?
        #     lda.save(str(sub_model_dir / f'model_{model_hash}.lda.bz2'))

        #     _logger.info(lda.print_topics())
        #     checkpoint_log(
        #         timer, _logger, message=f'Finished running model {model_num}/{models_count}...')
        #     # lda.update(corpus)
        #     # break


if __name__ == '__main__':
    # Use in local machine
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/test.yml -vv |& tee ./logs/train_lda_model.py.log
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/test.yml -vv --load-dictionary --from-dump |& tee ./logs/train_lda_model.py.log

    # Use in w1lxbdatad07
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/default.yml -vv |& tee ./logs/train_lda_model.py.log
    # python -u scripts/models/train_lda_model.py -c configs/models/lda/default.yml -vv --load-dictionary --from-dump |& tee ./logs/train_lda_model.py.log

    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script runs the LDA model training.
'''
import subprocess
import logging
from pathlib import Path
import os
import itertools
import json
import click
import gensim

import contexttimer
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
from wb_nlp.interfaces import mongodb

_logger = logging.getLogger(__file__)


def checkpoint_log(timer, logger, message=''):
    logger.info('Time elapsed now in minutes: %s %s',
                timer.elapsed / 60, message)


@click.command()
@click.option('-mcid', '--model-config-id', 'model_config_id', required=True,
              help='Configuration id for the configuration of the model that will be used.')
@click.option('-ccid', '--cleaning-config-id', 'cleaning_config_id', required=True,
              help='Configuration id of the cleaning pipeline used in cleaning the input data.')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(model_config_id: str, cleaning_config_id: str, log_level: int):
    '''
    Entry point for LDA model training script.
    '''
    with contexttimer.Timer() as timer:
        configure_logger(log_level)

        cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", cleaning_config_id))

        assert cleaned_docs_dir.exists()

        cleaned_corpus_id = subprocess.check_output("md5sum " + cleaned_docs_dir.resolve().__str__(
        ) + "/*/*.txt | awk '{print $1}' | md5sum | awk '{print $1}'", shell=True)

        # The previous command returns a binary value like this: `b'07591edc636a73eafe9bea6eb2aaf3a6\n'` so we convert to str.
        cleaned_corpus_id = cleaned_corpus_id.strip().decode('utf-8')

        model_configs_collection = mongodb.get_model_configs_collection()
        model_config = model_configs_collection.find_one(
            {"_id": model_config_id})

        model_name = model_config["meta"]["model_name"]

        assert model_name == "lda"
        assert gensim.__version__ == model_config['meta']['library_version']

        # corpus_path = paths_conf['corpus_path']
        file_generator = MultiDirGenerator(
            base_dir=cleaned_docs_dir.parent,
            source_dir_name=cleaned_docs_dir.name,
            split=True,
            min_tokens=model_config['min_tokens'],
            logger=_logger
        )

        _logger.info('Training dictionary...')
        dictionary_params = model_config['dictionary_config']

        processed_corpus_id = f"{cleaned_corpus_id}_{dictionary_params['dictionary_config_id']}"

        dictionary_file = cleaned_docs_dir / \
            f"dictionary-{processed_corpus_id}.gensim.dict"
        corpus_path = cleaned_docs_dir / f"bow_corpus-{processed_corpus_id}.mm"

        checkpoint_log(
            timer, _logger, message='Loading or generating dictionary...')

        if corpus_path.exists():
            _logger.info('Loading saved corpus and dictionary...')
            assert dictionary_file.exists()

            g_dict = Dictionary.load(str(dictionary_file))
            corpus = MmCorpus(corpus_path)

        else:
            if dictionary_file.exists():
                g_dict = Dictionary.load(str(dictionary_file))
            else:
                g_dict = Dictionary(file_generator)

                g_dict.filter_extremes(
                    no_below=dictionary_params['no_below'],
                    no_above=dictionary_params['no_above'],
                    keep_n=dictionary_params['keep_n'],
                    keep_tokens=dictionary_params['keep_tokens'])

                g_dict.id2token = {id: token for token,
                                   id in g_dict.token2id.items()}

                g_dict.save(str(dictionary_file))

            _logger.info('Generating corpus...')
            corpus = [g_dict.doc2bow(d) for d in file_generator]

            _logger.info('Saving corpus to %s...', corpus_path)
            MmCorpus.serialize(corpus_path, corpus)

        checkpoint_log(
            timer, _logger, message='Loading or generating corpus...')

        lda_params = model_config["lda_config"]
        lda_params['id2word'] = dict(g_dict.id2token)

        lda = LdaMulticore(corpus, **lda_params)

        model_run_info = dict(
            model_name=model_name,
            model_config_id=model_config_id,
            processed_corpus_id=processed_corpus_id,
        )
        model_run_info_id = generate_model_hash(
            model_run_info)

        model_run_info["model_run_info_id"] = model_run_info_id

        model_dir = dir_manager.get_path_from_root(
            "models", "lda", model_run_info_id)

        # TODO: Find a better strategy to name models.
        # It can be a hash of the config values for easier tracking?
        lda.save(str(model_dir / f'model_{model_run_info_id}.lda.bz2'))

        _logger.info(lda.print_topics())
        checkpoint_log(
            timer, _logger, message=f'Finished running {model_name} model for model_config {model_config_id} with run id {model_run_info_id}...')

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

        # model_dir = Path(dir_manager.get_path_from_root(
        #     paths_conf['model_dir']))
        # if not model_dir.exists():
        #     model_dir.mkdir(parents=True)

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

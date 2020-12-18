#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Script that runs the cleaning of raw text data given a configuration file.
'''
import re
import logging
from pathlib import Path
from typing import Callable
import click

from scipy.stats import beta
import pandas as pd
from nltk import sent_tokenize
import enchant
from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.cleaning import cleaner
from wb_nlp.utils.scripts import configure_logger, load_config, create_dask_cluster

en_dict = enchant.Dict('en_US')


def joblib_clean_file(
        cleaner_func: Callable[[str], list],
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")

        # tokens = lda_cleaner.get_clean_tokens(text)
        tokens = cleaner_func(text)

    output_file = output_dir / input_file.name

    with open(output_file, "w") as out_file:
        out_file.write(" ".join(tokens))

    return True


def filter_document_by_language(txt, pval=0.05):
    '''Remove contents of documents that are unlikely to be in English.

    This uses statistical hypothesis testing to automate the removal of tokens.
    '''

    alpha_pattern = re.compile(r'[a-z]+')
    dash_sub = re.compile(r'\s*-\s*')
    non_en_spell = []
    # sents = sent_tokenize(txt)
    sents = txt.split('\n')
    for idx in range(len(sents)):
        ssub = dash_sub.sub('', sents[idx].lower())
        tokens = alpha_pattern.findall(ssub)

        candidate_tokens = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                                       tokens))
        if not candidate_tokens:
            continue
        # Total number of tokens
        n = len(candidate_tokens)
        # number of success -> alpha parameter for the beta distribution.
        a = len(list(filter(en_dict.check, candidate_tokens)))
        # number of failures -> beta parameter for the beta distribution.
        b = n - a

        non_en_spell.append(
            {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'], means['b'])
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)

    return '\n'.join(non_en_spell_df[non_en_spell_df['pval'] > pval]['sent'])


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--config', 'cfg_path', required=True,
              type=click.Path(exists=True), help='path to yaml config file')
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--output-dir-name', 'output_dir_name', required=True, help='name of the output directory')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--non-recursive', 'recursive', flag_value=False, default=True)
@click.option('--recursive', 'recursive', flag_value=True)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(cfg_path: Path, input_dir: Path, output_dir_name: str, log_level: int, recursive: bool, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for cleaning raw text data inside a directory given a config file.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    cfg_path = Path(cfg_path)
    input_dir = Path(input_dir)

    _logger.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    source_dirs = [input_dir]
    target_dirs = []
    if recursive:
        # Assume that the input_directory is at the corpus level.
        # Example: input_dir = '/data/raw/CORPUS'
        # /data/raw/CORPUS/ADB/TXT_ORIG
        # /data/raw/CORPUS/WB/TXT_ORIG
        # Also, the output dir will be stored in the same path as the
        # parent of the input dir under the directory specified in the
        # output_dir parameter.
        source_dirs = sorted(input_dir.glob('*/TXT_ORIG'))
        target_dirs = [i.resolve().parent /
                       output_dir_name for i in source_dirs]
        _logger.info('List of source dirs... %s', source_dirs)
        _logger.info('List of target dirs... %s', target_dirs)
        assert source_dirs, "No source_dirs found. Aborting!"
    else:
        target_dirs.append(input_dir.resolve().parent / output_dir_name)

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    config = load_config(cfg_path, 'cleaner_config', _logger)

    cleaner_object = cleaner.BaseCleaner(
        config=config,
        include_pos=config['include_pos_tags'],
        exclude_entities=config['exclude_entity_types'],
        min_token_length=config['min_token_length'],
        max_token_length=config['max_token_length']
    )

    _logger.info('Starting joblib tasks...')
    files_count = 0
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        for input_dir, output_dir in zip(source_dirs, target_dirs):

            if not output_dir.exists():
                output_dir.mkdir(parents=True)

            res = Parallel(verbose=1, batch_size=batch_size)(
                delayed(joblib_clean_file)(
                    cleaner_object.get_clean_tokens,
                    ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

            files_count += len(res)
            _logger.info('Processed all %s files with success status %s and saved in %s', len(res),
                         all(res), output_dir)

    _logger.info('Processed a total of %s files across %s source dirs...',
                 files_count, len(source_dirs))
# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u ./scripts/cleaning/clean_corpus.py --config ./configs/cleaning/default.yml --input-dir ./data/raw/sample_data/TXT_SAMPLE --output-dir ./data/preprocessed/sample_data/clean_text -vv |& tee ./logs/clean_corpus.py.log
    # python -u ./scripts/cleaning/clean_corpus.py --config ./configs/cleaning/default.yml --input-dir ./data/raw/sample_data/TXT_SAMPLE --output-dir-name TXT_TEST -vv |& tee ./logs/clean_corpus.py.log
    main()

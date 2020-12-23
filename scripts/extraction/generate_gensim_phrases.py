#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script processes the text data to generate candidate phrases based on part-of-speech patterns.
'''
import logging
from pathlib import Path
from typing import Callable

import gzip
import json

import click

from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.cleaning import cleaner
from wb_nlp.utils.scripts import configure_logger, load_config, create_dask_cluster
from wb_nlp.types.cleaning import CleaningConfig

# logging.basicConfig(stream=sys.stdout,
#                     level=logging.INFO,
#                     datefmt='%Y-%m-%d %H:%M',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

MAX_LENGTH = 1000000


def joblib_extract_phrases(
        cleaner_func: Callable[[str], dict],
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function used in joblib to parallelize extraction of phrases across text documents.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")[:MAX_LENGTH]

        # result = lda_cleaner.get_tokens_and_phrases(text)
        # Output is a dictionary with keys `tokens` and `phrases`
        result = cleaner_func(text, return_phrase_count=True)

    output_file = output_dir / (input_file.name + '.json.gz')

    with gzip.open(output_file, mode='wt', encoding='utf-8') as gz_file:
        json.dump(result, gz_file)

    return True


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--config', 'cfg_path', required=True,
              type=click.Path(exists=True), help='path to yaml config file')
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--output-dir', 'output_dir', required=True,
              type=click.Path(exists=False), help='path to directory of output text files')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(cfg_path: Path, input_dir: Path, output_dir: Path, log_level: int):
    '''
    Entry point for part-of-speech based phrase generation script.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    cfg_path = Path(cfg_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    logging.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = create_dask_cluster(_logger)
    _logger.info(client)

    config = load_config(cfg_path, 'cleaning_config', _logger)
    config = CleaningConfig(**config).dict()

    cleaner_object = cleaner.BaseCleaner(config=config)

    _logger.info('Starting joblib tasks...')
    with joblib.parallel_backend('dask'):
        res = Parallel(verbose=10)(
            delayed(joblib_extract_phrases)(
                cleaner_object.get_tokens_and_phrases,
                ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

    _logger.info('Processed all: %s', all(res))

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u generate_phrases.py --config ../../configs/cleaning/default.yml --input-dir ../../data/raw/sample_data/TXT_SAMPLE --output-dir ../../data/preprocessed/sample_data/phrases -v |& tee generate_phrases.py.log
    main()

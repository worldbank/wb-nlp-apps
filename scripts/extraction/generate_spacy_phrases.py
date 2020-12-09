#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script processes the text data to generate candidate phrases based on part-of-speech patterns.
'''
import logging
from pathlib import Path
from collections import Counter
import gzip
import json

import click

from joblib import Parallel, delayed
import joblib
import spacy

import wb_nlp
from wb_nlp.extraction.phrase import get_spacy_phrases
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster

# logging.basicConfig(stream=sys.stdout,
#                     level=logging.INFO,
#                     datefmt='%Y-%m-%d %H:%M',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

MAX_LENGTH = 1000000

nlp = spacy.load("en_core_web_sm", disable=["parser"])


def joblib_extract_spacy_phrases(
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function used in joblib to parallelize extraction of phrases across text documents.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")[:MAX_LENGTH]

        doc = nlp(text)

        phrases = get_spacy_phrases(doc)
        phrases = dict(Counter(phrases).most_common())

        result = dict(lib='SpaCy', tokens=[], phrases=phrases)

    output_file = output_dir / (input_file.name + '.json.gz')

    with gzip.open(output_file, mode='wt', encoding='utf-8') as gz_file:
        json.dump(result, gz_file)

    return True


_logger = logging.getLogger(__file__)


@click.command()
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--output-dir', 'output_dir', required=True,
              type=click.Path(exists=False), help='path to directory of output text files')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(input_dir: Path, output_dir: Path, log_level: int, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for part-of-speech based phrase generation script.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    logging.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    _logger.info('Starting joblib tasks...')
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        res = Parallel(verbose=10, batch_size=batch_size)(
            delayed(joblib_extract_spacy_phrases)(
                ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

    _logger.info('Processed all: %s', all(res))

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u ./scripts/extraction/generate_spacy_phrases.py --input-dir ./data/raw/sample_data/TXT_SAMPLE --output-dir ./data/preprocessed/sample_data/spacy_phrases -v --n-workers 6 |& tee generate_spacy_phrases.py.log
    main()

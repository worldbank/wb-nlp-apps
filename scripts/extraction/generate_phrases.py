#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import sys
from typing import Callable
import click
from IPython.core import ultratb

import yaml

import dask
import dask.bag as db
import dask.dataframe as dd
from dask.distributed import get_worker
from dask.distributed import Client, LocalCluster, progress
from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.cleaning import cleaner
import gzip
import json
from contexttimer.timeout import timeout


def joblib_extract_phrases(cleaner_func: Callable[[str], dict], file_id: int, input_file: Path, output_dir: Path):
    # logging.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")

        # result = lda_cleaner.get_tokens_and_phrases(text)
        # Output is a dictionary with keys `tokens` and `phrases`
        result = cleaner_func(text)

    output_file = output_dir / (input_file.name + '.json.gz')

    with gzip.open(output_file, mode='wt', encoding='utf-8') as zf:
        json.dump(result, zf)

    return True


# fallback to debugger on error
sys.excepthook = ultratb.FormattedTB(
    mode='Verbose', color_scheme='Linux', call_pdb=1)

_logger = logging.getLogger(__name__)


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
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    cfg_path = Path(cfg_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    logging.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    logging.info('Creating dask client...')
    client = Client(threads_per_worker=1, processes=True)
    logging.info(client)
    logging.info(client.dashboard_link)

    logging.info(f'Load config file {cfg_path}...')
    with open(cfg_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
        config = config['config']

    cleaner_object = cleaner.BaseCleaner(
        config=config,
        include_pos=config['include_pos_tags'],
        exclude_entities=config['exclude_entity_types'],
        min_token_length=config['min_token_length'],
        max_token_length=config['max_token_length']
    )

    def timeout_handler(limit, f, *args, **kwargs):
        logging.warn(f"{f.__name__} timed out after {limit}s...")
        return False

    # @timeout(limit=5 * 60, handler=timeout_handler)
    def phrase_extractor_with_timeout(text: str):
        return cleaner_object.get_tokens_and_phrases(text)

    logging.info(f'Starting joblib tasks...')
    with joblib.parallel_backend('dask'):
        res = Parallel(verbose=10)(delayed(joblib_extract_phrases)(phrase_extractor_with_timeout, ix, i, output_dir)
                                   for ix, i in enumerate(input_dir.glob('*.txt'), 1))

    logging.info(f'Processed all: {all(res)}')

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python generate_phrases.py --config ../../configs/cleaning/default.yml --input-dir ../../data/raw/sample_data/TXT_SAMPLE --output-dir ../../data/preprocessed/sample_data/phrases -v
    main()

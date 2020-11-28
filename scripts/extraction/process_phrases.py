#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import os
import sys
from typing import Callable
import click
from IPython.core import ultratb

import gzip
import json
import yaml

from collections import Counter

import dask
import dask.bag as db
import dask.dataframe as dd
from dask.distributed import get_worker
from dask.distributed import Client, LocalCluster, progress
from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.cleaning import cleaner


# fallback to debugger on error
# sys.excepthook = ultratb.FormattedTB(
#     mode='Verbose', color_scheme='Linux', call_pdb=1)

_logger = logging.getLogger(__name__)


@click.command()
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--output-dir', 'output_dir', required=True,
              type=click.Path(exists=False), help='path to directory of output text files')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.version_option(wb_nlp.__version__)
def main(input_dir: Path, output_dir: Path, log_level: int):
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    logging.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    doc_frequency = Counter()
    total_frequency = Counter()

    for ix, input_file in enumerate(input_dir.glob('*.json.gz'), 1):
        if ix % 100 == 0:
            logging.info(f"{ix}. {input_file}")

        with gzip.open(input_file, mode='rt', encoding='utf-8') as zf:
            result = json.load(zf)

        doc_frequency.update(result['phrases'].keys())
        total_frequency.update(result['phrases'])

    doc_frequency_out = output_dir / 'phrases_doc_frequency.json'
    total_frequency_out = output_dir / 'phrases_total_frequency.json'

    with open(doc_frequency_out, 'w') as fl:
        json.dump(dict(doc_frequency.most_common()), fl)

    with open(total_frequency_out, 'w') as fl:
        json.dump(dict(total_frequency.most_common()), fl)

    logging.info(doc_frequency.most_common(100))


# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u process_phrases.py --input-dir ../../data/preprocessed/sample_data/phrases --output-dir ../../data/preprocessed/sample_data/phrases_processed -v
    main()

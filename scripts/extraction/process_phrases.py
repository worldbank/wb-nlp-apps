#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script aggregates the result of the generate_phrases.py script to
identify the most common part-of-speech based phrases in the corpus.
'''
import gzip
import json
import logging
import sys
from collections import Counter
from pathlib import Path

import click

import wb_nlp


# fallback to debugger on error
# sys.excepthook = ultratb.FormattedTB(
#     mode='Verbose', color_scheme='Linux', call_pdb=1)

_logger = logging.getLogger(__file__)


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
    '''
    Entry point for aggregating part-of-speech based phrases
    extracted from the generate_phrases.py script.
    '''
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    _logger.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    doc_frequency = Counter()
    total_frequency = Counter()

    for idx, input_file in enumerate(input_dir.glob('*.json.gz'), 1):
        if idx % 100 == 0:
            _logger.info("%s. %s", idx, input_file)

        with gzip.open(input_file, mode='rt', encoding='utf-8') as gz_file:
            result = json.load(gz_file)

        doc_frequency.update(result['phrases'].keys())
        total_frequency.update(result['phrases'])

    doc_frequency_out = output_dir / 'phrases_doc_frequency.json'
    total_frequency_out = output_dir / 'phrases_total_frequency.json'

    with open(doc_frequency_out, 'w') as open_file:
        json.dump(
            dict(filter(lambda x: x[1] > 1, doc_frequency.most_common())), open_file)

    with open(total_frequency_out, 'w') as open_file:
        json.dump(
            dict(filter(lambda x: x[1] > 1, total_frequency.most_common())), open_file)

    _logger.info(doc_frequency.most_common(100))


# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u process_phrases.py --input-dir ../../data/preprocessed/sample_data/phrases --output-dir ../../data/preprocessed/sample_data/phrases_processed -v
    main()

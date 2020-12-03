#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Script that runs the cleaning of raw text data given a configuration file.
'''
import logging
from pathlib import Path
from typing import Callable
import click


from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.cleaning import cleaner
from wb_nlp.utils.scripts import configure_logger, load_config, create_dask_cluster


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
    Entry point for cleaning raw text data inside a directory given a config file.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    cfg_path = Path(cfg_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    _logger.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = create_dask_cluster(_logger)
    _logger.info(client)

    config = load_config(cfg_path, 'config', _logger)

    cleaner_object = cleaner.BaseCleaner(
        config=config,
        include_pos=config['include_pos_tags'],
        exclude_entities=config['exclude_entity_types'],
        min_token_length=config['min_token_length'],
        max_token_length=config['max_token_length']
    )

    _logger.info('Starting joblib tasks...')
    with joblib.parallel_backend('dask'):
        res = Parallel(verbose=10)(
            delayed(joblib_clean_file)(
                cleaner_object.get_clean_tokens,
                ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

    _logger.info('Processed all: %s', all(res))

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # python -u clean_corpus.py --config ../../configs/cleaning/default.yml --input-dir ../../data/raw/sample_data/TXT_SAMPLE --output-dir ../../data/preprocessed/sample_data/clean_text -v |& tee clean_corpus.py.log
    main()

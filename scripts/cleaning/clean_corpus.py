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

from wb_nlp.dir_manager import get_data_dir
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster
from wb_nlp.interfaces import mongodb

MIN_TOKEN_COUNT = 10


def joblib_clean_file(
        cleaner_func: Callable[[str], list],
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    output_file = output_dir / input_file.name

    if not output_file.exists():
        with open(input_file, "rb") as in_file:
            text = in_file.read().decode("utf-8", errors="ignore")
            tokens = cleaner_func(text)

        if len(tokens) >= MIN_TOKEN_COUNT:
            text = " ".join(tokens).strip()

            with open(output_file, "w") as out_file:
                out_file.write(text)

    return True


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--cleaning-config-id', 'cleaning_config_id', required=True,
              help='Configuration id of the cleaning pipeline that will be used.')
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--source-dir-name', 'source_dir_name', required=False, help='name of the source directory', default="EN_TXT_ORIG")
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--non-recursive', 'recursive', flag_value=False, default=True)
@click.option('--recursive', 'recursive', flag_value=True)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(cleaning_config_id: Path, input_dir: Path, source_dir_name: str, log_level: int, recursive: bool, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for cleaning raw text data inside a directory given a config file.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_dir = Path(input_dir)

    cleaning_configs_collection = mongodb.get_cleaning_configs_collection()

    config = cleaning_configs_collection.find_one({"_id": cleaning_config_id})

    assert config

    _logger.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    source_dirs = [input_dir]
    target_dirs = []

    target_dir = Path(get_data_dir('corpus', 'cleaned', cleaning_config_id))

    if not target_dir.exists():
        _logger.info(
            "Target directory %s doesn't exist... Creating it now...", target_dir)
        target_dir.mkdir(parents=True)

    if recursive:
        # Assume that the input_directory is at the corpus level.
        # Example: input_dir = 'data/corpus'
        # data/corpus/ADB/EN_TXT_ORIG
        # data/corpus/WB/EN_TXT_ORIG
        # Also, the output dir will be stored in the same path as the
        # parent of the input dir under the directory specified in the
        # output_dir parameter.
        source_dirs = sorted(input_dir.glob(f'*/{source_dir_name}'))
        target_dirs = [target_dir / i.parent.name for i in source_dirs]
        _logger.info('List of source dirs... %s', source_dirs)
        _logger.info('List of target dirs... %s', target_dirs)
        assert source_dirs, "No source_dirs found. Aborting!"
    else:
        target_dirs.append(target_dir / input_dir.parent.name)

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    cleaner_object = cleaner.BaseCleaner(config=config)

    _logger.info('Starting joblib tasks...')
    files_count = 0
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        for input_dir, output_dir in zip(source_dirs, target_dirs):

            if not output_dir.exists():
                output_dir.mkdir(parents=True)

            res = Parallel(verbose=10, batch_size=batch_size)(
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
    # python -u ./scripts/cleaning/clean_corpus.py --cleaning-config-id 23f78350192d924e4a8f75278aca0e1c --input-dir data/corpus --source-dir-name EN_TXT_ORIG -vv |& tee ./logs/clean_corpus.py.log
    # python -u ./scripts/cleaning/clean_corpus.py --cleaning-config-id 229abf370f281efa7c9f3c4ddc20159d --input-dir data/corpus --source-dir-name EN_TXT_ORIG --recursive -vv |& tee ./logs/clean_corpus.py.log
    main()

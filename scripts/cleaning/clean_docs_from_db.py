#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Script that runs the cleaning of raw text data given a configuration id available in mongodb collection `nlp/cleaning_config`.
'''
import logging
from pathlib import Path
from typing import Callable
import click


from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.dir_manager import get_data_dir
from wb_nlp.cleaning import cleaner
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster
from wb_nlp.interfaces import mongodb


def joblib_clean_file(
        cleaner_func: Callable[[str], list],
        file_id: int, doc: dict,
        root_dir: Path,
        target_dir: Path, logger=None):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.
    '''

    input_file = root_dir / doc["path_original"]
    output_dir = target_dir / doc["corpus"]

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")
        tokens = cleaner_func(text)

    output_file = output_dir / input_file.name

    with open(output_file, "w") as out_file:
        out_file.write(" ".join(tokens))

    return True


_logger = logging.getLogger(__file__)


@click.command()
@click.option('-c', '--cleaning-config-id', 'cleaning_config_id', required=True,
              help='Configuration id of the cleaning pipeline that will be used.')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(cleaning_config_id: str, log_level: int, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for cleaning raw text data inside a directory given a config file.
    '''
    configure_logger(log_level)

    cleaning_configs_collection = mongodb.get_cleaning_configs_collection()
    # docs_metadata_collection = mongodb.get_docs_metadata_collection()
    docs_metadata_collection = mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")

    config = cleaning_configs_collection.find_one({"_id": cleaning_config_id})

    assert config

    target_dir = Path(get_data_dir('corpus', 'cleaned', cleaning_config_id))

    if not target_dir.exists():
        _logger.info(
            "Target directory %s doesn't exist... Creating it now...", target_dir)
        target_dir.mkdir(parents=True)

    # Get the root location /
    root_dir = target_dir.parent.parent.parent.parent

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    cleaner_object = cleaner.BaseCleaner(config=config)

    _logger.info('Starting joblib tasks...')
    files_count = 0
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        doc_iterator = docs_metadata_collection.find(
            projection=["_id", "path_original", "corpus"])

        res = Parallel(verbose=10, batch_size=batch_size)(
            delayed(joblib_clean_file)(
                cleaner_object.get_clean_tokens,
                ix, doc, root_dir, target_dir) for ix, doc in enumerate(doc_iterator, 1))

        files_count += len(res)
        _logger.info('Processed all %s files with success status %s and saved in %s', len(res),
                     all(res), target_dir)


if __name__ == '__main__':
    # python -u ./scripts/cleaning/clean_docs_from_db.py --cleaning-config-id 23f78350192d924e4a8f75278aca0e1c -vv |& tee ./logs/clean_docs_from_db.py.log

    main()

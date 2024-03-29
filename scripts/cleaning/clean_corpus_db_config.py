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
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster
from wb_nlp.interfaces import mongodb
from wb_nlp.dir_manager import get_data_dir


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
@click.option('-c', '--cleaning-config-id', 'cleaning_config_id', required=True,
              help='Configuration id of the cleaning pipeline that will be used.')
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--non-recursive', 'recursive', flag_value=False, default=True)
@click.option('--recursive', 'recursive', flag_value=True)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(cleaning_config_id: str, input_dir: Path, log_level: int, recursive: bool, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for cleaning raw text data inside a directory given a config file.
    '''
    configure_logger(log_level)

    input_dir = Path(input_dir)

    _logger.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    source_dirs = [input_dir]
    target_dirs = []
    if recursive:
        # Assume that the input_directory is at the corpus level.
        # Example: input_dir = 'data/corpus'
        # data/corpus/ADB/TXT_ORIG
        # data/corpus/WB/TXT_ORIG
        # Also, the output dir will be stored in the same path as the
        # `input_dir` under the cleaned/`cleaning_config_id` directory.
        source_dirs = sorted(input_dir.glob('*/TXT_ORIG'))
        target_dirs = [input_dir.resolve() / "cleaned" /
                       cleaning_config_id / i.parent.name for i in source_dirs]
        _logger.info('List of source dirs... %s', source_dirs)
        _logger.info('List of target dirs... %s', target_dirs)
        assert source_dirs, "No source_dirs found. Aborting!"
    else:
        # The input_dir is expected to point directly to the directory
        # containing the *.txt files.
        assert input_dir.name == "TXT_ORIG"

        target_dirs.append(input_dir.resolve().parent.parent / "cleaned" /
                           cleaning_config_id / input_dir.parent.name)

    cleaning_configs_collection = mongodb.get_cleaning_configs_collection()
    config = cleaning_configs_collection.find_one({"_id": cleaning_config_id})

    assert config

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
    # python -u ./scripts/cleaning/clean_corpus_db_config.py --cleaning-config-id 23f78350192d924e4a8f75278aca0e1c --input-dir ./data/corpus -vv |& tee ./logs/clean_corpus_db_config.py.log
    main()

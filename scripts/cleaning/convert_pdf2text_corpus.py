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
from wb_nlp.processing import document


def joblib_convert_file(
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    output_file = output_dir / f"{input_file.stem}.txt"

    if output_file.exists():
        return True

    pages = document.PDFDoc2Txt().parse(
        source=str(input_file.resolve()), source_type="file")

    with open(output_file, "w") as out_file:
        out_file.write(" ".join(pages))

    return True


_logger = logging.getLogger(__file__)


@click.command()
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
def main(input_dir: Path, log_level: int, recursive: bool, n_workers: int = None, batch_size: int = None):
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
        # data/corpus/ADB/PDF_ORIG
        # data/corpus/WB/PDF_ORIG
        # Also, the output dir will be stored in the same path as the
        # `input_dir` under the cleaned/`cleaning_config_id` directory.
        source_dirs = sorted(input_dir.glob('*/PDF_ORIG'))
        target_dirs = [input_dir.resolve() / i.parent.name / "TXT_ORIG"
                       for i in source_dirs]
        _logger.info('List of source dirs... %s', source_dirs)
        _logger.info('List of target dirs... %s', target_dirs)
        assert source_dirs, "No source_dirs found. Aborting!"
    else:
        # The input_dir is expected to point directly to the directory
        # containing the *.txt files.
        assert input_dir.name == "PDF_ORIG"

        target_dirs.append(input_dir.resolve().parent / "TXT_ORIG")

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    _logger.info('Starting joblib tasks...')
    files_count = 0
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        for input_dir, output_dir in zip(source_dirs, target_dirs):

            if not output_dir.exists():
                output_dir.mkdir(parents=True)

            res = Parallel(verbose=10, batch_size=batch_size)(
                delayed(joblib_convert_file)(ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.pdf'), 1))

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
    # python -u ./scripts/cleaning/convert_pdf2text_corpus.py --input-dir data/corpus --recursive -vv |& tee ./logs/convert_pdf2text_corpus.py.log
    main()

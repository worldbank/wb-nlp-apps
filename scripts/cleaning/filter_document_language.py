#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Script that runs the cleaning of raw text data given a configuration file.
'''
import re
import logging
from pathlib import Path
import click
from functools import lru_cache
from scipy.stats import beta
import pandas as pd
# from nltk import sent_tokenize
import enchant
from joblib import Parallel, delayed
import joblib
import wb_nlp
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster
# from wb_nlp import dir_manager

# en_dict_pwl = enchant.DictWithPWL('en_US', pwl=dir_manager.get_data_dir(
#     "whitelists", "whitelists", "wordfreq-enwiki-latest-pages-articles.xml.bz2.pwl.txt"))


# def dict_check(word, en_dict):
#     @lru_cache(maxsize=100000)
#     def check_word(word):
#         return en_dict.check(word)
#     return check_word


def joblib_filter_english_file(
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

    non_en_output_file = output_dir.parent / \
        "NON_EN_TXT_ORIG" / f"{input_file.stem}.txt"
    if not non_en_output_file.parent.exists():
        non_en_output_file.parent.mkdir(parents=True)

    with open(input_file, "rb") as open_file:
        text = open_file.read().decode("utf-8", errors="ignore")

        pval = 0.05
        non_en_spell_df = filter_document_by_language(text, return_df=True)

        en_txt = '\n'.join(
            non_en_spell_df[non_en_spell_df['pval'] > pval]['sent'])
        non_en_txt = '\n'.join(
            non_en_spell_df[non_en_spell_df['pval'] <= pval]['sent'])

        with open(output_file, "w") as out_file:
            out_file.write(en_txt)

        with open(non_en_output_file, "w") as non_en_out_file:
            non_en_out_file.write(non_en_txt)

    return True


def filter_document_by_language(txt, pval=0.05, en_dict=enchant.Dict("en_US"), return_en=True, return_df=False):
    '''Remove contents of documents that are unlikely to be in English.

    This uses statistical hypothesis testing to automate the removal of tokens.

    Other formulation:
    compute overlap in distribution of average (a, b) and the sentence.
    '''

    # delta = np.finfo(np.float).tiny
    delta = 1
    alpha_pattern = re.compile(r'[a-z]+')
    # In case a word is cut in newline
    newline_dash_sub = re.compile(r'(\S*)-\s+(\S*)')
    non_en_spell = []
    # sents = sent_tokenize(txt)
    txt = newline_dash_sub.sub(r'\1\2', txt)
    sents = txt.split('\n')
    for idx in range(len(sents)):
        sent = sents[idx].lower()
        tokens = alpha_pattern.findall(sent)

        candidate_tokens = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                                       tokens))
        if not candidate_tokens:
            continue
        # Total number of tokens
        n = len(candidate_tokens)
        # number of success -> alpha parameter for the beta distribution.
        a = len(list(filter(en_dict.check, candidate_tokens)))
        # number of failures -> beta parameter for the beta distribution.
        b = n - a

        non_en_spell.append(
            {'sent': sents[idx], 'clean': sent, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'] + delta, means['b'] + delta)
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)

    if return_df:
        return non_en_spell_df

    if return_en:
        filter_set = non_en_spell_df['pval'] > pval
    else:
        filter_set = non_en_spell_df['pval'] <= pval

    return '\n'.join(non_en_spell_df[filter_set]['sent'])


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
        # data/corpus/ADB/TXT_ORIG
        # data/corpus/WB/TXT_ORIG
        # Also, the output dir will be stored in the same path as the
        # `input_dir` under the cleaned/`cleaning_config_id` directory.
        source_dirs = sorted(input_dir.glob('*/TXT_ORIG'))
        target_dirs = [input_dir.resolve() / i.parent.name / "EN_TXT_ORIG"
                       for i in source_dirs]
        _logger.info('List of source dirs... %s', source_dirs)
        _logger.info('List of target dirs... %s', target_dirs)
        assert source_dirs, "No source_dirs found. Aborting!"
    else:
        # The input_dir is expected to point directly to the directory
        # containing the *.txt files.
        assert input_dir.name == "TXT_ORIG"

        target_dirs.append(input_dir.resolve().parent / "EN_TXT_ORIG")

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
                delayed(joblib_filter_english_file)(ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

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
    # python -u ./scripts/cleaning/filter_document_language.py --input-dir data/corpus --recursive -vv |& tee ./logs/filter_document_language.py.log
    main()

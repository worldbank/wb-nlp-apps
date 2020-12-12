'''
Module containing common functions used across the scripts.
'''
from pathlib import Path
import glob

from flashtext import KeywordProcessor
from wb_nlp import dir_manager
# export DASK_DISTRIBUTED__SCHEDULER__ALLOWED_FAILURES=210
# export DASK_DISTRIBUTED__COMM__TIMEOUTS__CONNECT=60
# export DASK_DISTRIBUTED__COMM__RETRY__COUNT=20

keyword_processor = KeywordProcessor()

with open(dir_manager.get_data_dir('whitelists', 'whitelists', 'phrases.txt')) as phrase_file:
    # Use flashtext format
    phrases_map = {l.strip(): [l.strip().replace('_', ' ')]
                   for l in phrase_file if l.strip()}
    keyword_processor.add_keywords_from_dict(phrases_map)


def load_file(fname: Path, split: bool = True):
    '''
    Simply loads a file and has an option to return the raw string or a list split by whitespaces.
    '''
    with open(fname) as open_file:
        txt = open_file.read()
        txt = keyword_processor.replace_keywords(txt)

    return txt.split() if split else txt


def generate_files(path: Path, split: bool = True, min_tokens: int = 50):
    '''
    A generator that loads text files given a directory.
    '''
    return filter(lambda x: len(x) >= min_tokens,
                  map(lambda x: load_file(x, split=split),
                      path.glob('*.txt')))


class MultiDirGenerator:
    def __init__(self, base_dir: str, source_dir_name: str = None, split: bool = True, min_tokens: int = 5, logger=None):
        self.base_dir = base_dir
        self.source_dir_name = source_dir_name
        self.split = split
        self.min_tokens = min_tokens
        self.logger = logger

        if source_dir_name is None:
            self.source_dirs = [Path(base_dir)]
        else:
            self.source_dirs = [Path(i) for i in glob.glob(
                f'{base_dir}/*/{source_dir_name}')]

        assert len(
            self.source_dirs) > 0, f"{base_dir}/*/{source_dir_name} doesn't exist!"

        for p in self.source_dirs:
            assert p.exists(), f"Path {p} doesn't exist!"

    def __iter__(self):
        for source_dir in self.source_dirs:
            if self.logger:
                self.logger.info(
                    'Loading files from source_dir %s', source_dir)
            for tokens in generate_files(source_dir, split=self.split, min_tokens=self.min_tokens):
                yield tokens

import glob
import numpy as np
import os
import pickle
import re
import spacy
import warnings
from enchant.checker import SpellChecker
from gensim.utils import simple_preprocess
from typing import Callable, Generator, Optional

from wb_nlp.extraction import extractor as extractor

# https://spacy.io/api/annotation
POS_TAGS = ['POS', 'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X', 'SPACE']

nlp = spacy.load('en_core_web_sm')
en = SpellChecker("en_US")


class BaseCleaner:

    def __init__(
        self, include_pos: tuple, exclude_entities: tuple,
        min_token_length: int=2, max_token_length: int=50,
        extractors: Optional[list]=None) -> None:

        self.include_pos = include_pos
        self.exclude_entities = exclude_entities
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length
        self.extractors = extractors or []  # extractor.CountryExtractor(nlp, lower=True)

    def clean_text(self, text: str) -> list:
        text = (
            text
            .replace('\n', ' ')
            .replace('’', "'")
            .replace('“', '"')
            .replace('”', '"')
        )

        text = re.sub(r'\s+', ' ', text).strip().lower()
        doc = nlp(text)

        for extractor in self.extractors:
            doc = extractor(doc)

        tokens = [token.lemma_ if token.lower_ != 'data' else 'data' for token in doc if self._is_valid_token(token)]
        # print((t.text, t.lemma_, t.pos_, t.ent_type_, t.ent_iob_, t._.normalized))

        return tokens

    def _is_valid_token(self, token: spacy.tokens.token.Token) -> bool:
        is_valid = token.ent_type_ not in self.exclude_entities
        is_valid = is_valid and token.pos_ in self.include_pos
        is_valid = is_valid and len(token) >= self.min_token_length
        is_valid = is_valid and len(token) <= self.max_token_length
        is_valid = is_valid and token.is_alpha

        return is_valid


class LDACleaner(BaseCleaner):
    LDA_INCLUDE_POS_TAGS = [
        'ADJ', 'NOUN',
        # 'VERB',
        # 'PROPN',
    ]

    LDA_EXCLUDE_ENT_TYPE = [
        'GPE', 'COUNTRY', 'PERSON','ORG',
        'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY',
        'ORDINAL',
        'CARDINAL',
    ]

    def __init__(
        self, min_token_length: int=2,
        max_token_length: int=50,
        extractors: Optional[list]=None) -> None:

        super(LDACleaner, self).__init__(
            LDACleaner.LDA_INCLUDE_POS_TAGS,
            LDACleaner.LDA_EXCLUDE_ENT_TYPE,
            min_token_length,
            max_token_length,
            extractors)


class Word2VecCleaner(BaseCleaner):

    EMBEDDING_INCLUDE_POS_TAGS = [
        'ADJ', 'NOUN', 'VERB',
        # 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ',
        # 'NUM', 'PART',
        'PROPN',
    ]

    EMBEDDING_EXCLUDE_ENT_TYPE = [
        'CARDINAL', 'TIME', 'PERCENT', 'MONEY',
        # 'DATE',
        # 'QUANTITY',
        # 'ORDINAL',
    ]

    def __init__(
        self, min_token_length: int=2,
        max_token_length: int=50,
        extractors: Optional[list]=None) -> None:

        super(Word2VecCleaner, self).__init__(
            Word2VecCleaner.EMBEDDING_INCLUDE_POS_TAGS,
            Word2VecCleaner.EMBEDDING_EXCLUDE_ENT_TYPE,
            min_token_length,
            max_token_length,
            extractors)


class SimpleCleaner(BaseCleaner):

    def __init__(self, min_token_length: int=2, max_token_length: int=50, extractors: Optional[list]=None) -> None:
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length

    def clean_text(self, text: str) -> list:
        return simple_preprocess(
            text, deacc=True,
            min_len=self.min_token_length,
            max_len=self.max_token_length)


class CorpusCleaner:
    '''This class manages the cleaning of files in a specified directory.

    Cleaned files are cached in the object to speed-up tasks the require the re-use
    of the cleaned data, e.g., phrase detection using gensim.

    A custom cleaner function can be used to handle the cleaning.
    '''

    def __init__(self,
        dir: str, cleaner: Callable[[str], str],
        id_pattern: Optional[str]=None,
        extension: str='txt', process_prob: float=1,
        seed: float=1029):

        self.dir = dir
        self.cleaner = cleaner
        self.id_pattern = id_pattern
        self.extension = extension
        self.process_prob = process_prob
        self.seed = seed

        self.clean_doc_cache = {}
        self.clean_doc_hash2id = {}
        self.clean_doc_id2hash = None

        self.clean_doc_generator = self.cleaned_doc_generator(
            dir, cleaner, id_pattern, extension
        )

        self.fully_trained = False
        self.frozen = False

    def check_train_state(self):
        if not self.fully_trained:
            raise ValueError('Corpus not fully processed!')

    def reset(self):
        self.check_train_state()

        self.clean_doc_generator = iter([
            self.clean_doc_cache[
                self.clean_doc_id2hash[id]] for id in sorted(self.clean_doc_id2hash)])

    def clear_docs(self):
        clear_keys = {
            'clean_doc_cache': {},
            'clean_doc_hash2id': {},
            'clean_doc_id2hash': None,
            'fully_trained': False,
            'frozen': False,
        }

        for k in list(self.__dict__):
            if k in clear_keys:
                del(self.__dict__[k])
                self.__dict__[k] = clear_keys[k]

        self.clean_doc_generator = self.cleaned_doc_generator(
            self.dir, self.cleaner, self.id_pattern, self.extension
        )

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.clean_doc_generator)

    def save(self, fname):
        self.check_train_state()

        valid_docs = [
            'dir', 'id_pattern', 'extension', 'frozen',
            'clean_doc_cache', 'clean_doc_hash2id',
            'clean_doc_id2hash', 'fully_trained',
            'process_prob', 'seed']

        payload = {key: self.__dict__[key] for key in valid_docs}

        with open(fname, 'wb') as fl:
            pickle.dump(payload, fl)

    def load(self, fname):
        with open(fname, 'rb') as fl:
            self.__dict__ = pickle.load(fl)

        self.frozen = True
        self.reset()

    def cleaned_doc_generator(
        self, dir: str, cleaner: Callable[[str], str],
        id_pattern: Optional[str]=None,
        extension: str='txt') -> Generator[list, None, None]:
        '''A generator that loads files from a directory and returns a cleaned document.
        This also caches the cleaned data.
        '''
        np.random.seed(self.seed)
        rands = np.random.random(10000000)

        doc_idx = 0

        for ix, fpath in enumerate(glob.glob(os.path.join(dir, f'*.{extension}'))):

            if self.process_prob < rands[ix]:
                continue

            fname = fpath.split('/')[-1]

            if id_pattern is None:
                file_hash = hash(fname)
            else:
                match = re.search(id_pattern, fname)
                if match:
                    file_hash = match.group(0)
                else:
                    warnings.warn(f'No valid id found in file {fname}. Skipping...')
                    continue

            if file_hash not in self.clean_doc_cache:
                with open(fpath, 'rb') as fl:
                    doc = fl.read().decode('utf-8', errors='ignore')
                    text = cleaner(doc)
                    self.clean_doc_cache[file_hash] = text

            self.clean_doc_hash2id[file_hash] = doc_idx
            doc_idx += 1

            yield self.clean_doc_cache[file_hash]

        self.clean_doc_id2hash = {j: i for i, j in self.clean_doc_hash2id.items()}
        self.fully_trained = True

    def stream_gensim_transformer(self, transformer, dictionary=None, cache=True):
        '''This function takes a suitable gensim transformer that takes a list of tokens as input.

        An example of this transformer is the Phraser transformer in gensim.

        If a dictionary is provided, it will automatically transform the document into a bag-of-word
        representation.
        '''
        self.check_train_state()
        self.reset()

        for cleaned_doc in self.__iter__():
            doc = [text for text in transformer[cleaned_doc]]

            if dictionary is not None:
                doc = dictionary.doc2bow(doc)

            yield doc

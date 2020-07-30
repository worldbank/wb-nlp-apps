import os
import re
import glob
import spacy
import warnings
from typing import Optional, Generator, Callable
from enchant.checker import SpellChecker
from gensim.utils import simple_preprocess

import wb_nlp.extraction.extractor as extractor

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
        extension: str='txt'):

        self.dir = dir
        self.cleaner = cleaner
        self.id_pattern = id_pattern
        self.extension = extension

        self.clean_doc_cache = {}
        self.clean_doc_hash2id = {}
        self.clean_doc_id2hash = None

        self.clean_doc_generator = self.cleaned_doc_generator(
            dir, cleaner, id_pattern, extension
        )

        self.fully_trained = False

    def check_train_state(self):
        if not self.fully_trained:
            raise ValueError('Corpus not fully processed!')

    def reset(self):
        self.check_train_state()

        if self.clean_doc_id2hash is None:
            self.clean_doc_id2hash = {j: i for i, j in self.clean_doc_hash2id.items()}

        self.clean_doc_generator = iter([
            self.clean_doc_cache[
                self.clean_doc_id2hash[id]] for id in sorted(self.clean_doc_id2hash)])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.clean_doc_generator)

    def cleaned_doc_generator(
        self, dir: str, cleaner: Callable[[str], str],
        id_pattern: Optional[str]=None,
        extension: str='txt') -> Generator[list, None, None]:
        '''A generator that loads files from a directory and returns a cleaned document.
        This also caches the cleaned data.
        '''
        doc_idx = 0

        for fpath in glob.glob(os.path.join(dir, f'*.{extension}')):
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

        self.fully_trained = True

    def stream_gensim_transformer(self, transformer, cache=True):
        '''This function takes a suitable gensim transformer that takes a list of tokens as input.

        An example of this transformer is the Phraser transformer in gensim.
        '''
        self.check_train_state()
        self.reset()

        for cleaned_doc in self.__iter__():
            yield [text for text in transformer[cleaned_doc]]

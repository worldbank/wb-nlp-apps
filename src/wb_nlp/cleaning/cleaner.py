"""Main cleaner module.
"""

import glob
import os
import pickle
import re
import warnings
from collections import Counter
from typing import Callable, Generator, Optional
from gensim.utils import simple_preprocess

import spacy
import numpy as np

import wb_nlp.config as conf
from wb_nlp.cleaning import stopwords, respelling
from wb_nlp.extraction import phrase
# from wb_nlp.extraction import extractor

# https://spacy.io/api/annotation
POS_TAGS = ["POS", "ADJ", "ADP", "ADV", "AUX", "CONJ", "CCONJ", "DET", "INTJ", "NOUN",
            "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X", "SPACE", ]

nlp = spacy.load("en_core_web_sm", disable=["parser"])
nlp.Defaults.stop_words |= set(stopwords.stopwords)


def expand_acronyms(text: str) -> str:
    # Parse acronyms here and replace instances.
    # Apply intelligent matching.
    return text


class BaseCleaner:
    def __init__(self, config: dict, include_pos: tuple, exclude_entities: tuple,
                 min_token_length: int = 2, max_token_length: int = 50,
                 extractors: Optional[list] = None) -> None:

        self.include_pos = include_pos
        self.exclude_entities = exclude_entities
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length
        self.extractors = (
            extractors or []
        )  # extractor.CountryExtractor(nlp, lower=True)

        self.set_config(config)

        self.spelling_model = respelling.SpellingModels(config)

    @staticmethod
    def text_to_doc(text: str) -> spacy.tokens.doc.Doc:
        """Performs basic normalization and converts text to spacy document.

        NOTE:
            Don't make the text here in lower case since we need to preserve
            the case for the extractors.

        """
        text = (
            text.replace("\n", " ")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
        )

        text = re.sub(r"\s+", " ", text).strip()
        doc = nlp(text)

        return doc

    def set_config(self, config):
        self.config = config

    def _apply_extractors(self, doc: spacy.tokens.doc.Doc) -> spacy.tokens.doc.Doc:
        """This updates the document to integrate information on tokens, e.g., names of countries.
        """
        for extractor in self.extractors:
            doc = extractor(doc)

        return doc

    def _tokenize(self, doc: spacy.tokens.doc.Doc) -> list:
        tokens = [
            token.lemma_.lower() if token.lower_ != "data" else "data"
            for token in doc
            if self._is_valid_token(token)
        ]

        return tokens

    def get_clean_tokens(self, text: str) -> list:
        # Fix not properly parsed tokens.
        if self.config["cleaner"]["fix_fragmented_tokens"]["use"]:
            text = self.spelling_model.recover_segmented_words(
                text, **self.config["cleaner"]["fix_fragmented_tokens"]["params"]
            )

        if self.config["cleaner"]["expand_acronyms"]["use"]:
            # Expand acronyms
            text = expand_acronyms(text)

        doc = BaseCleaner.text_to_doc(text)

        if self.config["cleaner"]["tag_whitelisted_entities"]["use"]:
            doc = self._apply_extractors(doc)

        tokens = self._tokenize(doc)

        if self.config["cleaner"]["correct_misspelling"]["use"]:
            tokens = self.spelling_model.fix_spellings(tokens)

        return tokens

    def get_clean_text(self, text: str) -> str:
        return " ".join(self.get_clean_tokens(text))

    def get_tokens_and_phrases(self, text: str, return_phrase_count: bool = False) -> dict:
        doc = BaseCleaner.text_to_doc(text)
        doc = self._apply_extractors(doc)
        tokens = []

        # tokens = self._tokenize(doc)
        phrases = phrase.get_phrases(
            doc,
            min_token_length=self.min_token_length,
            token_func=self._is_valid_token,
            token_container=tokens,
        )

        if return_phrase_count:
            phrases = dict(Counter(phrases).most_common())

        return dict(tokens=tokens, phrases=phrases)

    def _is_valid_token(self, token: spacy.tokens.token.Token) -> bool:
        is_valid = token.is_alpha
        is_valid = is_valid and len(token) >= self.min_token_length
        is_valid = is_valid and len(token) <= self.max_token_length

        # Check only for complex filters once the token passed the basic filters.
        if is_valid:

            if self.config["cleaner"]["filter_by_pos"]["use"]:
                is_valid = is_valid and (token.pos_ in self.include_pos)

            if self.config["cleaner"]["filter_by_entities"]["use"]:
                is_valid = is_valid and (
                    token.ent_type_ not in self.exclude_entities)

            if self.config["cleaner"]["filter_stopwords"]["use"]:
                is_valid = is_valid and not token.is_stop

        return is_valid


class LDACleaner(BaseCleaner):
    LDA_INCLUDE_POS_TAGS = [
        "ADJ",
        "NOUN",
        # 'PROPN',
        "VERB",
        # Which is better? Add this by default or simply create
        # a whitelist of relevant adverbs?
        "ADV",
    ]

    LDA_EXCLUDE_ENT_TYPE = [
        "GPE", "COUNTRY",  # Countries, cities, states
        "PERSON", "ORG",  # Persons and organizations
        "DATE", "TIME",  # Tomorrow, today, 10am, etc.
        "PERCENT", "MONEY", "QUANTITY",  # Words related to amounts and money
        "ORDINAL",  # first, second, etc.
        "CARDINAL",  # Other numerals
    ]

    def __init__(self, config: dict,
                 min_token_length: int = 2, max_token_length: int = 50,
                 extractors: Optional[list] = None) -> None:

        super(LDACleaner, self).__init__(
            config,
            LDACleaner.LDA_INCLUDE_POS_TAGS,
            LDACleaner.LDA_EXCLUDE_ENT_TYPE,
            min_token_length,
            max_token_length,
            extractors,
        )


class Word2VecCleaner(BaseCleaner):

    EMBEDDING_INCLUDE_POS_TAGS = [
        "ADJ",
        "NOUN",
        "VERB",
        # 'PROPN',
        # Which is better? Add this by default or simply create
        # a whitelist of relevant adverbs?
        "ADV"
        # 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ',
        # 'NUM', 'PART',
    ]

    EMBEDDING_EXCLUDE_ENT_TYPE = [
        "CARDINAL",
        "TIME",
        "PERCENT",
        "MONEY",
        # 'DATE',
        # 'QUANTITY',
        # 'ORDINAL',
    ]

    def __init__(self, config: dict,
                 min_token_length: int = 2, max_token_length: int = 50,
                 extractors: Optional[list] = None) -> None:

        super(Word2VecCleaner, self).__init__(
            config,
            Word2VecCleaner.EMBEDDING_INCLUDE_POS_TAGS,
            Word2VecCleaner.EMBEDDING_EXCLUDE_ENT_TYPE,
            min_token_length,
            max_token_length,
            extractors,
        )


class SimpleCleaner(BaseCleaner):
    def __init__(self, min_token_length: int = 2, max_token_length: int = 50,
                 extractors: Optional[list] = None) -> None:
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length

    def clean_text(self, text: str) -> list:
        return simple_preprocess(
            text,
            deacc=True,
            min_len=self.min_token_length,
            max_len=self.max_token_length,
        )


class CorpusCleaner:
    """This class manages the cleaning of files in a specified directory.

    Cleaned files are cached in the object to speed-up tasks the require the re-use
    of the cleaned data, e.g., phrase detection using gensim.

    A custom cleaner function can be used to handle the cleaning.
    """

    def __init__(self, dir: str, cleaner: Callable[[str], str],
                 id_pattern: Optional[str] = None, extension: str = "txt",
                 process_prob: float = 1, seed: float = 1029) -> None:

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
            raise ValueError("Corpus not fully processed!")

    def reset(self):
        self.check_train_state()

        self.clean_doc_generator = iter(
            [
                self.clean_doc_cache[self.clean_doc_id2hash[id]]
                for id in sorted(self.clean_doc_id2hash)
            ]
        )

    def clear_docs(self):
        clear_keys = {
            "clean_doc_cache": {},
            "clean_doc_hash2id": {},
            "clean_doc_id2hash": None,
            "fully_trained": False,
            "frozen": False,
        }

        for k in list(self.__dict__):
            if k in clear_keys:
                del self.__dict__[k]
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
            "dir",
            "id_pattern",
            "extension",
            "frozen",
            "clean_doc_cache",
            "clean_doc_hash2id",
            "clean_doc_id2hash",
            "fully_trained",
            "process_prob",
            "seed",
        ]

        payload = {key: self.__dict__[key] for key in valid_docs}

        with open(fname, "wb") as fl:
            pickle.dump(payload, fl)

    def load(self, fname):
        with open(fname, "rb") as fl:
            self.__dict__ = pickle.load(fl)

        self.frozen = True
        self.reset()

    def cleaned_doc_generator(self, dir: str, cleaner: Callable[[str], str],
                              id_pattern: Optional[str] = None, extension: str = "txt") -> Generator[list, None, None]:
        """A generator that loads files from a directory and returns a cleaned document.
        This also caches the cleaned data.
        """
        np.random.seed(self.seed)
        rands = np.random.random(10000000)

        doc_idx = 0

        for index, fpath in enumerate(glob.glob(os.path.join(dir, f"*.{extension}"))):

            if self.process_prob < rands[index]:
                continue

            fname = fpath.split("/")[-1]

            if id_pattern is None:
                file_hash = hash(fname)
            else:
                match = re.search(id_pattern, fname)
                if match:
                    file_hash = match.group(0)
                else:
                    warnings.warn(
                        f"No valid id found in file {fname}. Skipping...")
                    continue

            if file_hash not in self.clean_doc_cache:
                with open(fpath, "rb") as fl_rb:
                    doc = fl_rb.read().decode("utf-8", errors="ignore")
                    text = cleaner(doc)
                    self.clean_doc_cache[file_hash] = text

            self.clean_doc_hash2id[file_hash] = doc_idx
            doc_idx += 1

            yield self.clean_doc_cache[file_hash]

        self.clean_doc_id2hash = {j: i for i,
                                  j in self.clean_doc_hash2id.items()}
        self.fully_trained = True

    def stream_gensim_transformer(self, transformer, dictionary=None, cache=True):
        """This function takes a suitable gensim transformer that takes a list of tokens as input.

        An example of this transformer is the Phraser transformer in gensim.

        If a dictionary is provided, it will automatically transform the document into a bag-of-word
        representation.
        """
        self.check_train_state()
        self.reset()

        for cleaned_doc in self.__iter__():
            doc = list(transformer[cleaned_doc])

            if dictionary is not None:
                doc = dictionary.doc2bow(doc)

            yield doc


if __name__ == "__main__":
    bc = LDACleaner(conf.get_config(conf.default_config))

    t = bc.get_clean_tokens(
        """Hello world, why are you all here at the World Bank?
        We need to do something about the linear regresion.
        The bayesian information is not liot here."""
    )
    print(t)

    assert t == [
        "hello",
        "world",
        "need",
        "linear",
        "regression",
        "bayesian",
        "information",
    ]

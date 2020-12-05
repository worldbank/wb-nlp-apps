"""This module handles the recovery of words that may have been misparsed or misspelled.
"""
# Actual service dependencies
import itertools
import os
import re
import wordninja
import numpy as np
import pandas as pd

from enchant.checker import SpellChecker
from enchant import Dict
from joblib import Memory

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.metrics.distance import edit_distance
from scipy.stats import rankdata

from wb_nlp.cleaning.stopwords import stopwords
from wb_nlp.ops.cache_utils import redis_cacher

# Setup caching mechanism for speedup.
# Take note that `get_suggestions` using enchant is
# quite slow (~75% of the `cached_infer_correct_word` function).

USE_JOBLIB_MEMORY = False

if USE_JOBLIB_MEMORY:
    RESPELLER_CACHE_LOCATION = "/dev/shm/respeller-cachedir"
    respeller_cache = Memory(RESPELLER_CACHE_LOCATION, verbose=0)

    cache_decorator = respeller_cache.cache
else:
    cache_decorator = redis_cacher

# # Returns self without any form of caching.
# cache_decorator = lambda f: f

en_dict = Dict("en_US")


@cache_decorator
def get_suggestions(word: str, **kwargs) -> list:
    """Wrapper the caches the result of enchant's suggest method.

    Args:
        word:
            Word to check for suggestions.

    Returns:
        A list containing the most likely correct words based on enchant's dictionary.

    """
    return en_dict.suggest(word)


# @cache_decorator
# def en_dict_check(word, **kwargs):
#     # High overhead. Uncached speed ~100us vs cached speed ~500us
#     return en_dict.check(word)


def morph_word(word: str) -> str:
    """Apply simple morphing of the word to improve robustness for checking similarity.

    A derived token is created by concatenating the word and the sorted version of the word.

    Args:
        word:
            Word to be morphed.

    Returns:
        The morphed word.

    """
    # word = word.replace(' ', '')  # Check if compound word suggestion matches the misspelled word
    # Perform this opperation to add more robustness to the matching
    m_word = word + "".join(sorted(word))

    return m_word


@cache_decorator
def cached_infer_correct_word(
        word: str, sim_thresh: float = 0.0, print_log: bool = False,
        min_len: int = 3, use_suggest_score: bool = True, **kwargs) -> dict:
    """This method computes the inference score for the input word.

    Args:
        word:
            This is the misspelled word that requires checking for fix.
        sim_thresh:
            Similarity threshold to use to check if the candidate is
            acceptable.
            The similarity is derived based on character similarity
            and rank based on enchant's suggestions.
        print_log:
            Option to print the payload.
        min_len:
            Minimum length of token to check.
            If less than the `min_len`, don't attempt to fix.
        use_suggest_score:
            Flag whether to use the rank of enchant's suggestion in
            computing for the similarity score.
        **kwargs:
            Needed for caching (`argument_hash`)

    Returns:
        A dictionary containing the information of the inference.

    """
    # To collect cached data, execute the line below.
    # redis.hgetall('cleaner/respelling/cached_infer_correct_word')
    correct_word = None
    score = -1

    payload = dict(
        word=word,
        correct_word=correct_word,
        score=score,
        sim_thresh=sim_thresh,
        print_log=print_log,
        min_len=min_len,
        use_suggest_score=use_suggest_score,
    )

    if len(word) <= min_len:
        return payload

    candidates = get_suggestions(word, argument_hash=word)

    if use_suggest_score:
        suggest_score = 1 / rankdata(range(len(candidates))) ** 0.5
    else:
        suggest_score = np.ones(len(candidates))

    if candidates:
        try:
            m_word = morph_word(word)
            m_candidates = [morph_word(c.lower()) for c in candidates]

            tfidf = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
            cand_vecs = tfidf.fit_transform(m_candidates)
            word_vec = tfidf.transform([m_word])

            rank_score = 1.0 / rankdata([edit_distance(m_word, x)
                                         for x in m_candidates])

            sim = cosine_similarity(cand_vecs, word_vec)
            sim_r = sim * \
                rank_score.reshape(-1, 1) * suggest_score.reshape(-1, 1)

            sim_ind = sim_r.argmax()
            score = sim_r[sim_ind]
            if score > sim_thresh:
                correct_word = candidates[sim_ind]
        except Exception:
            print(f"Error word: {word}")

    if print_log:
        print(sim_r)
        print(rank_score)
        print(word)
        print(candidates)
        print(candidates[sim_ind])

    payload["correct_word"] = correct_word
    payload["score"] = float(score)

    return payload


class Respeller:
    """
    Use https://joblib.readthedocs.io/en/latest/auto_examples/memory_basic_usage.html#sphx-glr-auto-examples-memory-basic-usage-py
    to efficiently cache data for parallel computing.
    """

    def __init__(self, dictionary_file=None, spell_threshold=0.25,
                 allow_proper=False, spell_cache=None):
        """This respelling module tries to recover some misspelled words.
        This is done using enchant and text mining methods.

        Args:
            allow_proper:
                If set to True, this option allows suggestions that are
                proper nouns (first letter is capitalized).

                This seems ok to use if entity-based and pos-tag-based filters
                have already been applied prior to the respelling.

        """
        self.spell_cache = spell_cache if spell_cache is not None else {}  # pd.Series()
        self.dictionary_file = dictionary_file
        self.spell_threshold = spell_threshold
        self.allow_proper = allow_proper
        self.stopwords = set(stopwords)

        """
        TODO: Find a way to use an adaptive spell_threshold based on the length of the word.
        """

        if (self.dictionary_file is not None) and os.path.isfile(self.dictionary_file):
            self.spell_cache = pd.read_csv(self.dictionary_file)

    def save_spell_cache(self):
        """Option to save the local cache to a file.

        Make sure that the target file is not None (default).

        """
        assert self.dictionary_file is not None
        pd.Series(self.spell_cache).to_csv(self.dictionary_file)

    def infer_correct_word(
            self, word, sim_thresh=0.0, print_log=False,
            min_len=3, use_suggest_score=True):
        """Try to infer the correct word for a single misspelled word.

        Args:
            word:
                This is the misspelled word that requires checking for fix.
            sim_thresh:
                Similarity threshold to use to check if the candidate is
                acceptable.
                The similarity is derived based on character similarity
                and rank based on enchant's suggestions.
            print_log:
                Option to print the payload.
            min_len:
                Minimum length of token to check.
                If less than the `min_len`, don't attempt to fix.
            use_suggest_score:
                Flag whether to use the rank of enchant's suggestion in
                computing for the similarity score.

        Returns:
            A dictionary containing the payload for the word.

        """
        if word not in self.spell_cache:
            # Implement internal caching as well since Memory is still slow
            # due to its utilization of disk.
            payload = cached_infer_correct_word(
                word,
                sim_thresh=sim_thresh,
                print_log=print_log,
                min_len=min_len,
                use_suggest_score=use_suggest_score,
                argument_hash=word,
            )

            self.spell_cache[word] = payload

        return self.spell_cache[word]

    def qualified_word(self, word: str) -> bool:
        """Checks for the validity of the word.

        Filters such as stopwords, title case, and length are applied
        to check of the candidate word is actually valid.

        Args:
            word:
                Word to be tested for validity.

        Returns:
            The validity of the word.

        """
        is_valid = (
            (word not in stopwords)
            and ((not word[0].isupper()) or self.allow_proper)
            and len(word) > 2
        )

        return is_valid

    def infer_correct_words(
            self, words: list, return_tokens_as_list: bool,
            infer_correct_word_params: dict) -> [set, dict]:
        """Applies the inference of correct words to a list of input words.

        Args:
            words:
                List of misspelled tokens found using the spell checker.
            return_tokens_as_list:
                Option whether to return a list of list or list of strings.
                list of list handles the case for compound word suggestions.
                The value for this option is dependent on the use-case.
            infer_correct_word_params:
                This contains the parameters that controls how the
                `infer_correct_word` method behaves.
                Ideally, this should be defined in the config files.

        Returns:
            - A set object containing the misspelled words that were not fixed.
            - A dictionary with key corresponding to the misspelled word
                and value the fixed word.

        """
        respelled_set = {}
        unfixed_words = set([])

        for error_words in words:
            res = self.infer_correct_word(
                error_words, **infer_correct_word_params)

            word = res["word"]
            correct_word = res["correct_word"]
            score = res["score"]

            if correct_word and score > self.spell_threshold:
                if correct_word.istitle() and not self.allow_proper:
                    # If the respelling results to a `Title` word
                    # it implies that the word is a proper noun, therefore, omit.
                    unfixed_words.add(word)
                else:
                    # Split and filter since some words are compound terms.
                    respelled_set[word] = [
                        i.lower()
                        for i in correct_word.split()
                        if self.qualified_word(i)
                    ]

                    if not return_tokens_as_list:
                        respelled_set[word] = " ".join(respelled_set[word])

            else:
                unfixed_words.add(word)

        return unfixed_words, respelled_set


class OptimizedSpellChecker(SpellChecker):
    """
    Reduces the tokens only to unique words in the text. Output is not in the same order relative
    to the original text.
    """

    dict_words = set()

    def __init__(self, lang=None, text=None,
                 tokenize=None, chunkers=None, filters=None):
        super().__init__(
            lang=lang, text=text, tokenize=tokenize, chunkers=chunkers, filters=filters
        )

    def set_tokens(self, tokens):
        """Set the text to be spell-checked.

        This method must be called, or the 'text' argument supplied
        to the constructor, before calling the 'next()' method.

        """
        self._tokens = enumerate(tokens)

    def next(self):
        """Process text up to the next spelling error.

        This method is designed to support the iterator protocol.
        Each time it is called, it will advance the 'word' attribute
        to the next spelling error in the text.  When no more errors
        are found, it will raise StopIteration.

        The method will always return self, so that it can be used
        sensibly in common idioms such as:
            for err in checker:
                err.do_something()

        """
        # Find the next spelling error.
        # The uncaught StopIteration from next(self._tokens)
        # will provide the StopIteration for this method
        while True:
            pos, word = next(self._tokens)
            if word in self.dict_words:
                continue
            if self.dict.check(word):
                self.dict_words.add(word)
                continue
            if word in self._ignore_words:
                continue
            self.word = word
            self.wordpos = pos
            if word in self._replace_words:
                self.replace(self._replace_words[word])
                continue
            break
        return self


# General Text Processors
class SpellingModels:
    """
    This class holds the needed methods to abstract the fixing of
    misspelled and fragmented words.
    """

    def __init__(self, config: dict):
        self.config = config

        self.spell_checker = OptimizedSpellChecker(
            **self.config["spell_checker"]["__init__"]
        )
        self.respeller = Respeller(**self.config["respeller"]["__init__"])

    def fix_spellings(self, tokens: list) -> list:
        """This is the main method that handles the fixing of misspelled words.

        Args:
            tokens:
                Input tokens that have already been filtered and tokenized.

        Returns:
            A list of tokens with unrecoverable misspelled words removed.
            Misspelled words having a viable fix are replaced.

        """
        self.spell_checker.set_tokens(tokens)

        unfixed_tokens, fixed_tokens_map = self.respeller.infer_correct_words(
            [err_word.word for err_word in self.spell_checker],
            infer_correct_word_params=self.config["respeller"]["infer_correct_word"],
            **self.config["respeller"]["infer_correct_words"],
        )

        tokens = list(
            itertools.chain.from_iterable(
                [
                    fixed_tokens_map.get(token, [token])
                    for token in tokens
                    if token not in unfixed_tokens
                ]
            )
        )

        return tokens

    @staticmethod
    def recover_segmented_words(raw_input: str, max_len: int = 5) -> str:
        """This algorithm processes and input text to detect and fix any malformed words.

        Example:
            input: "million p rote c te d   by u n h c r Of the world's displaced"
            output: "million protected by unhcr Of the world's displaced"

        """

        alpha_streak = 0
        word_streak = 0
        val_span = ""
        temp_span = ""
        ends_space = False
        spaces = {" ", "\n", "\t"}

        # Handle plural form of acronyms, e.g., IDPs -> IDP
        raw_text = re.sub(r"(\W[A-Z]{2,})(s)(\W)", r"\1\3", raw_input)

        text = ""

        for i in raw_text:
            if i.isalpha():
                alpha_streak += 1
                temp_span += i
                ends_space = False
            else:
                if (alpha_streak and alpha_streak <= max_len) or (val_span and ends_space):
                    if i in spaces:
                        val_span += temp_span + i
                        word_streak += 1
                        temp_span = ""
                        # Speeds up processing vs. using val_span[-1].isspace()!
                        ends_space = True
                        alpha_streak = 0
                        continue

                if word_streak >= 2:
                    text += " ".join(wordninja.split("".join(val_span.split())))
                    text += " " + temp_span + i
                else:
                    text += val_span + temp_span + i

                word_streak = 0
                temp_span = ""
                val_span = ""
                ends_space = False
                alpha_streak = 0

        return text

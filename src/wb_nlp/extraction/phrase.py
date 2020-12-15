'''
This module contains methods that processes texts to extract phrases.
'''
from typing import Callable, Optional
import functools

import spacy
import nltk

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet


PHRASE_FILLERS = ['of', 'the', 'in']  # Not used if
SPACY_PHRASE_POS = ['ADJ', 'NOUN']  # , 'ADV']
NLTK_PHRASE_POS = ['JJ', 'NN']  # , 'RB']
PHRASE_SEP = '_'

NLTK_TAG_MAP = {
    'J': wordnet.ADJ,
    'N': wordnet.NOUN,
    # 'R': wordnet.ADV
}

SPACY_LIB = 'SpaCy'
NLTK_LIB = 'NLTK'

wordnet_lemmatizer = WordNetLemmatizer()


@functools.lru_cache(maxsize=1024)
def get_nltk_lemma(token, pos):
    return wordnet_lemmatizer.lemmatize(token, pos=NLTK_TAG_MAP.get(pos[0], wordnet.NOUN)).lower()


def generate_phrase(phrase_tokens: list, phrase_pos: list, library: str):
    '''This function generates a valid phrase from a list of tokens.

    Additionally, the function removes dangling PHRASE_FILLERS if present.

    library should be either SpaCy or NLTK.
    '''

    noun_form = 'NOUN' if library == 'SpaCy' else 'NN'

    valid_set = False
    for phpos in phrase_pos:
        if phpos.startswith(noun_form):
            valid_set = True
            break

    if not valid_set:
        return None

    while True and phrase_tokens:
        if not phrase_pos[-1].startswith(noun_form):
            phrase_tokens.pop(-1)
            phrase_pos.pop(-1)
        else:
            break

    sub_phrase = []
    for idx, i in enumerate(phrase_pos[::-1]):
        if not i.startswith(noun_form):
            if idx > 1:
                sub_phrase = PHRASE_SEP.join(phrase_tokens[-idx:])
            break

    phrases = [PHRASE_SEP.join(phrase_tokens)]
    if sub_phrase:
        phrases.append(sub_phrase)

    return phrases if len(phrase_tokens) > 1 else None


def get_spacy_phrases(
        doc: spacy.tokens.doc.Doc, min_token_length: int = 3,
        token_func: Optional[Callable] = None,
        token_container: Optional[list] = None) -> list:
    '''This function extracts phrases from a text based on the part-of-speech tag.

    Contiguous tokens with POS tag of NOUN/ADJ and optionally "fillers" in between
    are considered as phrases.

    The output of this can then be used with Gensim's Phrases model to filter valid phrases.
    '''

    phrases = []
    curr_phrase = []
    curr_pos_set = []

    for token in doc:

        # Collect tokens if `token_func` is provided.
        # This paradigm is used in wb_nlp.cleaning.cleaner.BaseCleaner.get_tokens_and_phrases.
        if token_func and token_func(token):
            token_container.append(
                token.lemma_ if token.lower_ != 'data' else 'data')

        if not (token.is_alpha and len(token) >= min_token_length):
            if token.text == '-':
                continue

            if len(curr_phrase) > 1:
                phrase = generate_phrase(
                    curr_phrase, curr_pos_set, library=SPACY_LIB)
                if phrase:
                    phrases.extend(phrase)

            curr_phrase = []
            curr_pos_set = []
            continue

        if len(curr_phrase) > 0 and token.lower_ in PHRASE_FILLERS:
            # This will not really work if we only use 'ADJ' and 'NOUN'.
            # But leaving this here in case we want to capture compound 'PROPN'.
            curr_phrase.append(token.lemma_)
            curr_pos_set.append(token.pos_)
        elif token.pos_ in SPACY_PHRASE_POS:
            curr_phrase.append(
                token.lemma_ if token.lower_ != 'data' else 'data')
            curr_pos_set.append(token.pos_)
        else:
            if len(curr_phrase) > 1:
                phrase = generate_phrase(
                    curr_phrase, curr_pos_set, library=SPACY_LIB)
                if phrase:
                    phrases.extend(phrase)
            curr_phrase = []
            curr_pos_set = []

    return phrases


def get_nltk_phrases(text: str, min_token_length: int = 3):
    '''
    Phrases extraction using NLTK.
    '''
    phrases = []
    curr_phrase = []
    curr_pos_set = []

    doc = nltk.pos_tag(nltk.word_tokenize(text))

    for token, pos in doc:
        NLTK_TAG_MAP.get(pos[0])

        if not (token.isalpha() and len(token) >= min_token_length):
            if token == '-':
                continue

            if len(curr_phrase) > 1:
                phrase = generate_phrase(
                    curr_phrase, curr_pos_set, library=NLTK_LIB)
                if phrase:
                    phrases.extend(phrase)

            curr_phrase = []
            curr_pos_set = []
            continue

        if len(curr_phrase) > 0 and token.lower() in PHRASE_FILLERS:
            # This will not really work if we only use 'JJ' and 'NN'.
            # But leaving this here in case we want to capture compound 'PROPN'.
            curr_phrase.append(token)
            curr_pos_set.append(pos)
        elif pos in NLTK_PHRASE_POS:
            curr_phrase.append(
                get_nltk_lemma(token, pos) if token.lower() != 'data' else 'data')
            curr_pos_set.append(pos)
        else:
            if len(curr_phrase) > 1:
                phrase = generate_phrase(
                    curr_phrase, curr_pos_set, library=NLTK_LIB)
                if phrase:
                    phrases.extend(phrase)
            curr_phrase = []
            curr_pos_set = []

    return phrases

import spacy
from typing import Callable, Optional


PHRASE_FILLERS = ['of', 'the', 'in']  # Not used if
PHRASE_POS = ['ADJ', 'NOUN', 'ADV']
PHRASE_SEP = '_'


def generate_phrase(phrase_tokens: list, phrase_pos: list):
    '''This function generates a valid phrase from a list of tokens.

    Additionally, the function removes dangling PHRASE_FILLERS if present.
    '''
    if 'NOUN' not in phrase_pos:
        return None

    while True and phrase_tokens:
        if phrase_pos[-1] != 'NOUN':
            phrase_tokens.pop(-1)
            phrase_pos.pop(-1)
        else:
            break

    sub_phrase = []
    for ix, i in enumerate(phrase_pos[::-1]):
        if i != 'NOUN':
            if ix > 1:
                sub_phrase = PHRASE_SEP.join(phrase_tokens[-ix:])
            break

    phrases = [PHRASE_SEP.join(phrase_tokens)]
    if sub_phrase:
        phrases.append(sub_phrase)

    return phrases if len(phrase_tokens) > 1 else None


def get_phrases(
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
                phrase = generate_phrase(curr_phrase, curr_pos_set)
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
        elif token.pos_ in PHRASE_POS:
            curr_phrase.append(
                token.lemma_ if token.lower_ != 'data' else 'data')
            curr_pos_set.append(token.pos_)
        else:
            if len(curr_phrase) > 1:
                phrase = generate_phrase(curr_phrase, curr_pos_set)
                if phrase:
                    phrases.extend(phrase)
            curr_phrase = []
            curr_pos_set = []

    return phrases

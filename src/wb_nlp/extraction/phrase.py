import spacy
from typing import Callable, Optional


PHRASE_FILLERS = ['of', 'the', 'in']  # Not used if
PHRASE_POS = ['ADJ', 'NOUN']

def generate_phrase(phrase_tokens):
    '''This function generates a valid phrase from a list of tokens.

    Additionally, the function removes dangling PHRASE_FILLERS if present.
    '''

    while True and phrase_tokens:
        if phrase_tokens[-1] in PHRASE_FILLERS:
            phrase_tokens.pop()
        else:
            break

    return '_'.join(phrase_tokens) if len(phrase_tokens) > 1 else None


def get_phrases(
    doc: spacy.tokens.doc.Doc, min_token_length: int=3,
    token_func: Optional[Callable]=None,
    token_container: Optional[list]=None) -> list:
    '''This function extracts phrases from a text based on the part-of-speech tag.

    Contiguous tokens with POS tag of NOUN/ADJ and optionally "fillers" in between
    are considered as phrases.

    The output of this can then be used with Gensim's Phrases model to filter valid phrases.
    '''

    phrases = []
    curr_phrase = []

    for token in doc:

        # Collect tokens if `token_func` is provided.
        # This paradigm is used in wb_nlp.cleaning.cleaner.BaseCleaner.get_tokens_and_phrases.
        if token_func and token_func(token):
            token_container.append(token.lemma_ if token.lower_ != 'data' else 'data')

        if not (token.is_alpha and len(token) >= min_token_length):
            if token.text == '-':
                continue

            if len(curr_phrase) > 1:
                phrase = generate_phrase(curr_phrase)
                if phrase:
                    phrases.append(phrase)

            curr_phrase = []
            continue

        if len(curr_phrase) > 0 and token.lower_ in PHRASE_FILLERS:
            # This will not really work if we only use 'ADJ' and 'NOUN'.
            # But leaving this here in case we want to capture compound 'PROPN'.
            curr_phrase.append(token.lemma_)
        elif token.pos_ in PHRASE_POS:
            curr_phrase.append(token.lemma_ if token.lower_ != 'data' else 'data')
        else:
            if len(curr_phrase) > 1:
                phrase = generate_phrase(curr_phrase)
                if phrase:
                    phrases.append(phrase)
            curr_phrase = []

    return phrases

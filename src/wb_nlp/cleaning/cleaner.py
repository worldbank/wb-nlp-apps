import re
import spacy
from typing import Optional
from enchant.checker import SpellChecker
import wb_nlp.extraction.extractor as extractor

# https://spacy.io/api/annotation
POS_TAGS = ['POS', 'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X', 'SPACE']

nlp = spacy.load('en_core_web_sm')
en = SpellChecker("en_US")


class BaseCleaner:

    def __init__(self, include_pos: tuple, exclude_entities: tuple, min_token_length: int=2, extractors: Optional[list]=None) -> None:
        self.include_pos = include_pos
        self.exclude_entities = exclude_entities
        self.min_token_length = min_token_length
        self.extractors = extractors or []  # extractor.CountryExtractor(nlp, lower=True)

    def clean_text(self, text: str) -> list:
        text = (
            text
            .replace('\n', ' ')
            .replace('’', "'")
            .replace('“', '"')
            .replace('”', '"')
        )

        text = re.sub('\s+', ' ', text).strip().lower()
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

    def __init__(self, min_token_length: int=2, extractors: Optional[list]=None) -> None:

        super(LDACleaner, self).__init__(
            LDACleaner.LDA_INCLUDE_POS_TAGS,
            LDACleaner.LDA_EXCLUDE_ENT_TYPE,
            min_token_length,
            extractors)


class Word2VecCleaner(BaseCleaner):

    EMBEDDING_INCLUDE_POS_TAGS = [
        'ADJ', 'NOUN', 'VERB',
        # 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ',
        # 'NUM', 'PART',
        'PROPN',
    ]

    EMBEDDING_INVALID_ENT_TYPE = [
        'CARDINAL', 'TIME', 'PERCENT', 'MONEY',
        # 'DATE',
        # 'QUANTITY',
        # 'ORDINAL',
    ]

    def __init__(self, min_token_length: int=2, extractors: Optional[list]=None) -> None:

        super(Word2VecCleaner, self).__init__(
            Word2VecCleaner.EMBEDDING_INCLUDE_POS_TAGS,
            Word2VecCleaner.EMBEDDING_EXCLUDE_ENT_TYPE,
            min_token_length,
            extractors)

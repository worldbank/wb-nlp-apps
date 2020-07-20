#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token


class BaseExtractor:
    name = 'base_extractor'

    def __init__(self, nlp, entities: tuple, label: str, extractor_id: str, callback=None, mapping=None):
        self.label = label
        self.label_id = nlp.vocab.strings[label]
        self.extractor_id = extractor_id
        self.attribute_id = self.extractor_id.lower()
        self.mapping = mapping

        patterns = [nlp(ent) for ent in entities]
        self.extractor = PhraseMatcher(nlp.vocab)
        self.extractor.add(extractor_id, callback, *patterns)

        Token.set_extension(f'is_{self.attribute_id}', default=False, force=True)

        if self.mapping is not None:
            Token.set_extension(f'normalized', default='', force=True)

        # Register and implement attribute and getter in subclasses.

    def __call__(self, doc):
        extracted = self.extractor(doc)
        spans = []
        with doc.retokenize() as retokenizer:
            for id, start, end in extracted:
                entity = doc[start:end]  # Span(doc, start, end, label=self.label_id)
                # spans.append(entity)

                for token in entity:
                    token._.set('normalized', self.mapping.get(entity.text, entity.text))
                    token._.set(f'is_{self.attribute_id}', True)
                    token.ent_type_ = self.label

                retokenizer.merge(entity)

        return doc


class CountryExtractor(BaseExtractor):

    def __init__(self, nlp, entities: tuple, label: str='COUNTRY', extractor_id: str='COUNTRY'):
        self.country_mapping = CountryExtractor.load_country_mapping()
        super(CountryExtractor, self).__init__(nlp, entities, label, extractor_id, None, self.country_mapping)

    @staticmethod
    def load_country_mapping():
        return {'Philippines': 'Philippines', 'Pilipinas': 'Philippines', 'Sri Lanka': 'Sri Lanka'}

        # # Register attributes on Doc and Span via a getter that checks if one of
        # # the contained tokens is set to is_tech_org == True.
        # Doc.set_extension("has_tech_org", getter=self.has_tech_org)
        # Span.set_extension("has_tech_org", getter=self.has_tech_org)

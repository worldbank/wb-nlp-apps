import spacy


def get_phrases(doc: spacy.tokens.doc.Doc, min_token_length: int=3):
    phrases = []
    curr_phrase = []

    for token in doc:
        # if token.ent_type_:
        #     curr_phrase = []
        #     continue

        if not (token.is_alpha and len(token) >= min_token_length):
            if token.text == '-':
                continue

            if len(curr_phrase) > 1:
                phrases.append('_'.join(curr_phrase))

            curr_phrase = []
            continue

        if token.pos_ in ['ADJ', 'NOUN']:
            curr_phrase.append(token.lemma_ if token.lower_ != 'data' else 'data')
        else:
            if len(curr_phrase) > 1:
                phrases.append('_'.join(curr_phrase))
            curr_phrase = []

    return phrases

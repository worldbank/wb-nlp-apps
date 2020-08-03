import spacy


def get_phrases(doc: spacy.tokens.doc.Doc, min_token_length: int=3):
    phrases = []
    curr_phrase = []
    fillers = ['of', 'the', 'in']  # Not used if

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

        if len(curr_phrase) > 0 and token.lower_ in fillers:
            # This will not really work if we only use 'ADJ' and 'NOUN'.
            # But leaving this here in case we want to capture compound 'PROPN'.
            curr_phrase.append(token.lemma_)
        elif token.pos_ in ['ADJ', 'NOUN']:
            curr_phrase.append(token.lemma_ if token.lower_ != 'data' else 'data')
        else:
            if len(curr_phrase) > 1:
                while True:
                    if curr_phrase[-1] in fillers:
                        curr_phrase.pop()
                    else:
                        break

                phrases.append('_'.join(curr_phrase))
            curr_phrase = []

    return phrases

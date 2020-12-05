
default_config=dict(
    cleaner_config=dict(
        # Options for cleaning.corrector.recover_segmented_words
        fix_fragmented_tokens=dict(
            use=True,
            params=dict(
                max_len=5,
            )
        ),
        # Expand the acronyms in the text
        expand_acronyms=dict(
            use=True,
            params=dict()
        ),
        # Update the spacy doc with the whitelisted entitiy tag
        tag_whitelisted_entities=dict(
            use=True,
            params=dict()
        ),
        # Use the part-of-speech as filter
        filter_by_pos=dict(
            use=True,
            params=dict()
        ),
        # Use extracted entities as filter
        filter_by_entities=dict(
            use=True,
            params=dict()
        ),
        # Check and fix spelling based on the Respeller module
        correct_misspelling=dict(
            use=True,
            params=dict()
        ),
        # Remove stopwords from the text
        filter_stopwords=dict(
            use=True,
            params=dict()
        ),
    ),

    spell_checker_config=dict(
        __init__=dict(
            lang='en_US',
            text=None,
            tokenize=None,
            chunkers=None,
            filters=None,
        )
    ),

    respeller_config=dict(
        __init__=dict(
            dictionary_file=None,
            spell_threshold=0.25,
            allow_proper=True,
            spell_cache=None),
        infer_correct_word=dict(
            sim_thresh=0.0,
            print_log=False,
            min_len=3,
            use_suggest_score=True,
        ),
        infer_correct_words=dict(
            return_tokens_as_list=True,
        )
    ),
)

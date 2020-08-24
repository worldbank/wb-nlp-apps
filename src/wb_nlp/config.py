default_cleaner_config = dict(
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
    check_spelling=dict(
        use=True,
        params=dict()
    ),
    # Remove stopwords from the text
    filter_stopwords=dict(
        use=True,
        params=dict()
    ),
)

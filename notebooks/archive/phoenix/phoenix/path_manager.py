import os

# ./SCRIPTS
# ROOT_DIR = os.path.abspath(os.pardir)
# ROOT_DIR = '/R/NLP'
ROOT_DIR = (
    os.path.dirname( # ./wb-nlp/
        os.path.dirname( # ./wb-nlp/phoenix
            os.path.dirname( # ./wb-nlp/phoenix/phoenix
                os.path.abspath(__file__)
            )
        )
    )
)
CORPUS_DIR = os.path.join(
    ROOT_DIR,  # /NLP
    'CORPUS'
)

MODELS_DIR = os.path.join(
    ROOT_DIR,  # /NLP
    'MODELS'
)

def get_models_path(model_id):
    return os.path.join(MODELS_DIR, model_id)

def get_corpus_path(corpus_id):
    return os.path.join(CORPUS_DIR, corpus_id)

def get_txt_orig_path(corpus_id):
    return os.path.join(get_corpus_path(corpus_id), 'TXT_ORIG')

def get_txt_clean_path(corpus_id):
    return os.path.join(get_corpus_path(corpus_id), 'TXT_CLEAN')

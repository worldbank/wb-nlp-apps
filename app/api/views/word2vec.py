# WORD2VEC
import os
import glob
import requests
import json
import numpy as np
import pandas as pd
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
from services.word2vec_module import Word2VecModel
from views.cleaning import clean_text
from services.metadata import get_document_metadata
from services.translation import translate
import werkzeug
from flask import request
import langdetect
from utils.parser import parse_args, log_payload
import werkzeug

from wb_nlp.dir_manager import get_model_dir


headers = {"Content-Type": "application/json", "Accept": "application/json"}
cleaning_url = 'http://localhost:8910/api/clean_text'
WVEC_MODELS_PATH = get_model_dir('WORD2VEC')
WVEC_MODELS = {}


parser_wv = reqparse.RequestParser()
parser_wv.add_argument(
    'raw_text', type=str,
    required=True, help='raw text input required'
)
parser_wv.add_argument(
    'corpus_id', type=str,
    required=True, help='Corpus used to train the word2vec model.'
)
parser_wv.add_argument(
    'model_id', type=str,
    required=True, help='Identification for the model defined by the corpus partition and vector dimension.'
)
parser_wv.add_argument(
    'clean_doc', type=boolean,
    required=True, help='Specifies whether cleaning should be done on the raw_text.'
)
parser_wv.add_argument(
    'use_ngram', type=boolean,
    required=False, help='Flag to choose if ngram transformed text will be used.'
)
parser_wv.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files',
    required=False, help='File to upload.'
)


def load_model(corpus_id, model_id, workers=1):
    # No doc_df for now.
    corpus_part, num_topics = model_id.split('_')
    # Handles the format where we use other parameters: 128.wdw3 m-> 128 dimensions and window = 3
    num_topics = num_topics.split('.')[0]
    num_topics = int(num_topics)

    w2vec_model = Word2VecModel(
        doc_df=None,
        corpus_id=corpus_id,
        model_id=model_id,
        dim=num_topics,
        workers=workers,
        model_path=WVEC_MODELS_PATH,
        # optimize_interval=0,
        # iter=5
    )

    w2vec_model.load()

    return w2vec_model


def get_model(corpus_id, model_id):
    if corpus_id not in WVEC_MODELS:
        WVEC_MODELS[corpus_id] = {model_id: load_model(corpus_id, model_id)}
    else:
        if model_id not in WVEC_MODELS[corpus_id]:
            WVEC_MODELS[corpus_id][model_id] = load_model(corpus_id, model_id)

    return WVEC_MODELS.get(corpus_id, {}).get(model_id)


class Word2VecView(Resource):
    def post(self):
        args = parser_wv.parse_args()

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        should_clean = args['clean_doc']
        use_ngram = args['use_ngram']

        if args.get('file') is not None:
            file = args['file']
            text = file.read()
            try:
                text = text.decode('utf-8', 'ignore')
            except:
                return {'Error': "File can't be decoded."}
        elif args.get('raw_text') is not None:
            text = args['raw_text']
        else:
            return {'Error': 'Please provide a file or a raw_text parameter.'}

        # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        model = get_model(corpus_id, model_id)
        if model is None:
            return {}

        # Clean document first.
        if should_clean:
            text = clean_text(text)
            if not use_ngram:
                text = text.get('text')
            else:
                text = text.get('ngram_text', text.get('text'))

        vector = model.transform_doc(text)

        return {'vector': vector.flatten().tolist() if isinstance(vector, np.ndarray) else vector}

    def get(self):
        return self.post()


parser_word2vec = reqparse.RequestParser()
parser_word2vec.add_argument(
    'raw_text', type=str,
    required=False, help='raw text input required'
)
parser_word2vec.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files',
    required=False, help='File to upload.'
)
parser_word2vec.add_argument(
    'topn', type=int, default=10,
    required=False, help='Number of similar docs or words to return.'
)
parser_word2vec.add_argument(
    'corpus_id', type=str, default='WB',
    required=False, help='Corpus used to train the word2vec model.'
)
parser_word2vec.add_argument(
    'model_id', type=str, default='ALL_100',
    required=False, help='Identification for the model defined by the corpus partition and vector dimension.'
)
parser_word2vec.add_argument(
    'clean_doc', type=boolean, default=True,
    required=False, help='Specifies whether cleaning should be done on the raw_text.'
)
parser_word2vec.add_argument(
    'use_ngram', type=boolean, default=True,
    required=False, help='Flag to choose if ngram transformed text will be used.'
)
parser_word2vec.add_argument(
    'show_duplicates', type=boolean, default=False,
    required=False, help='Flag that indicates whether to return highly similar or possibly duplicate documents.'
)
parser_word2vec.add_argument(
    'duplicate_threshold', type=float, default=0.98,
    required=False, help='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
)
parser_word2vec.add_argument(
    'return_related_words', type=boolean, default=True,
    required=False, help='Flag indicating an option to return similar or topic words to the document.'
)
parser_word2vec.add_argument(
    'id', type=str, default='',
    required=False, help='Valid id of document in corpus.'
)
parser_word2vec.add_argument(
    'show_duplicates', type=boolean, default=False,
    required=False, help='Flag that indicates whether to return highly similar or possibly duplicate documents.'
)
parser_word2vec.add_argument(
    'duplicate_threshold', type=float, default=0.98,
    required=False, help='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
)
parser_word2vec.add_argument(
    'return_related_words', type=boolean, default=True,
    required=False, help='Flag indicating an option to return similar or topic words to the document.'
)
parser_word2vec.add_argument(
    'log_output', type=boolean, default=True,
    required=False, help='Flag indicating an option to log output.'
)
parser_word2vec.add_argument(
    'translate', type=boolean, default=True,
    required=False, help='Flag indicating an option to translate the input data.'
)


def check_translate_text(text, apply_translate):
    if apply_translate:
        lang = langdetect.detect(text)

        if lang != 'en':
            result = translate(text)
            if 'translated' in result:
                text = result['translated']

    return text


def preprocess_input(args):
    corpus_id = args['corpus_id']
    model_id = args['model_id']
    should_clean = args['clean_doc']
    topn = args['topn']
    use_ngram = args['use_ngram']

    if args.get('file') is not None:
        file = args['file']
        text = file.read()
        try:
            text = text.decode('utf-8', 'ignore')
        except:
            return {'Error': "File can't be decoded."}

    elif args.get('raw_text') is not None:
        text = args['raw_text']
    else:
        return {'Error': 'Please provide a file or a raw_text parameter.'}

    text = check_translate_text(text, apply_translate=args['translate'])

    model = get_model(corpus_id, model_id)
    if model is None:
        return {'Error': f'No model found for {corpus_id}-{model_id}'}

    # Clean document first.
    if should_clean:
        text = clean_text(text)
        if not use_ngram:
            text = text.get('text')
        else:
            text = text.get('ngram_text', text.get('text'))

    payload = {'text': text, 'model': model, 'topn': topn}

    if args['log_output']:
        _payload = dict(payload)
        _payload['model'] = f'{corpus_id}-{model_id}'
        log_payload(_payload)

    return payload


class RelatedWordsView(Resource):
    def post(self):
        args = parse_args(parser_word2vec)

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']
        topn = output['topn']

        payload = pd.read_json(
            model.get_similar_words(text, topn=topn, serialize=True)
        ).to_dict('records')
        payload = sorted(payload, key=lambda x: x['rank'])
        for p in payload:
            p['score'] = np.round(p['score'], decimals=5)

        payload = {'words': payload}

        if args['log_output']:
            log_payload(payload)

        return payload

    def get(self):
        return self.post()


class RelatedDocsView(Resource):
    def post(self):
        args = parse_args(parser_word2vec)

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']
        topn = output['topn']
        show_duplicates = args['show_duplicates']
        duplicate_threshold = args['duplicate_threshold']
        return_related_words = args['return_related_words']

        payload = pd.read_json(
            model.get_similar_documents(
                text, topn=topn, serialize=True,
                duplicate_threshold=duplicate_threshold,
                show_duplicates=show_duplicates,
            )
        ).to_dict('records')
        payload = sorted(payload, key=lambda x: x['rank'])
        for p in payload:
            p['score'] = np.round(p['score'], decimals=5)

        for p in payload:
            p['metadata'] = get_document_metadata(p['id'])

        related_words = []
        if return_related_words:
            related_words = pd.read_json(
                model.get_similar_words(text, topn=topn, serialize=True)
            ).to_dict('records')
            related_words = sorted(related_words, key=lambda x: x['rank'])
            for rw in related_words:
                rw['score'] = np.round(rw['score'], decimals=5)

        payload = {'docs': payload, 'words': related_words}

        if args['log_output']:
            # Don't include the metadata in the logs
            _payload = {
                'docs': [{'id': p['id'], 'score': p['score'], 'rank': p['rank']} for p in payload['docs']],
                'words': payload['words']
            }
            log_payload(_payload)

        return payload

    def get(self):
        return self.post()


class RelatedDocsByIDView(Resource):
    def post(self):
        args = parse_args(parser_word2vec)

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        id = args['id']
        topn = args['topn']
        show_duplicates = args['show_duplicates']
        duplicate_threshold = args['duplicate_threshold']
        return_related_words = args['return_related_words']

        # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        model = get_model(corpus_id, model_id)
        if model is None:
            return {}

        payload = pd.read_json(
            model.get_similar_docs_by_id(
                id, topn=topn, serialize=True,
                duplicate_threshold=duplicate_threshold,
                show_duplicates=show_duplicates,
            )
        ).to_dict('records')
        payload = sorted(payload, key=lambda x: x['rank'])

        for p in payload:
            p['score'] = np.round(p['score'], decimals=5)

        for p in payload:
            p['metadata'] = get_document_metadata(p['id'])

        related_words = []
        if return_related_words:
            related_words = pd.read_json(
                model.get_similar_words_by_id(id, topn=topn, serialize=True)
            ).to_dict('records')
            related_words = sorted(related_words, key=lambda x: x['rank'])
            for rw in related_words:
                rw['score'] = np.round(rw['score'], decimals=5)

        payload = {'docs': payload, 'words': related_words}

        if args['log_output']:
            # Don't include the metadata in the logs
            _payload = {
                'docs': [{'id': p['id'], 'score': p['score'], 'rank': p['rank']} for p in payload['docs']],
                'words': payload['words']
            }
            log_payload(_payload)

        return payload

    def get(self):
        return self.post()

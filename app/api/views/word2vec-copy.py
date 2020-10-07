### WORD2VEC
import path_manager
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
from services.metadata import get_documents_metadata
import werkzeug
from flask import request


headers = {"Content-Type": "application/json", "Accept": "application/json"}
cleaning_url = 'http://localhost:8910/api/clean_text'
WVEC_MODELS_PATH = path_manager.get_models_path('WORD2VEC')
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


def load_model(corpus_id, model_id, workers=1):
    # No doc_df for now.
    corpus_part, num_topics = model_id.split('_')
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

    
# for saved_model_file in glob.iglob(os.path.join(WVEC_MODELS_PATH, '*-w2vec*.mm')):
#    print(f'Loading {saved_model_file}...')
#    model_name = os.path.basename(saved_model_file)
#    # model_name -> imf-w2vec_ALL_50.mm
#    corpus_id, parts = model_name.strip('.mm').split('-')
#    corpus_id = corpus_id.upper()
#    model_id = parts.replace('w2vec_', '')
#
#    if corpus_id in WVEC_MODELS:
#        WVEC_MODELS[corpus_id][model_id] = load_model(corpus_id, model_id)
#    else:
#        WVEC_MODELS[corpus_id] = {model_id: load_model(corpus_id, model_id)}


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
        text = args['raw_text']
        should_clean = args['clean_doc']
        use_ngram = args['use_ngram']
        
        model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        if model is None:
            return {}
        
        # Clean document first.
        if should_clean:
            text = clean_text(text)
            if not use_ngram:
                text = text.get('text')
            else:
                text = text.get('ngram_text', text.get('text'))
            # data = requests.post(cleaning_url, data=json.dumps({'raw_text': text}), headers=headers)
            # if data.status_code != 200:
            #     return {}
            
            # text = data.json()['text']
        
        vector = model.transform_doc(text)
        
        return {'vector': vector.flatten().tolist() if isinstance(vector, np.ndarray) else vector}

    def get(self):
        return self.post()

    
parser_related_words = reqparse.RequestParser()
parser_related_words.add_argument(
    'raw_text', type=str,
    required=False, help='raw text input required'
)
parser_related_words.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files',
    required=False, help='File to upload.'
)
parser_related_words.add_argument(
    'topn', type=int, default=10,
    required=False, help='Number of similar words to return.'
)
parser_related_words.add_argument(
    'corpus_id', type=str, default='IMF',
    required=False, help='Corpus used to train the word2vec model.'
)
parser_related_words.add_argument(
    'model_id', type=str, default='ALL_50',
    required=False, help='Identification for the model defined by the corpus partition and vector dimension.'
)
parser_related_words.add_argument(
    'clean_doc', type=boolean, default=True,
    required=False, help='Specifies whether cleaning should be done on the raw_text.'
)
parser_related_words.add_argument(
    'use_ngram', type=boolean, default=False,
    required=False, help='Flag to choose if ngram transformed text will be used.'
)

def preprocess_input(args):
    print(args)

    corpus_id = args['corpus_id']
    model_id = args['model_id']
    should_clean = args['clean_doc']
    topn = args['topn']
    use_ngram = args['use_ngram']

    if args.get('file') is not None:
        file = args['file']
        print(file)
        text = file.read()
        try:
            text = text.decode('utf-8', 'ignore')
        except:
            return {'Error': "File can't be decoded."}
            
    elif args.get('raw_text') is not None:
        text = args['raw_text']
    else:
        return {'Error': 'Please provide a file or a raw_text parameter.'}

    model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
    if model is None:
        return {'Error': f'No model found for {corpus_id}-{model_id}'}
    
    # Clean document first.
    if should_clean:
        text = clean_text(text)
        if not use_ngram:
            text = text.get('text')
        else:
            text = text.get('ngram_text', text.get('text'))
        # data = requests.post(cleaning_url, data=json.dumps({'raw_text': text}), headers=headers)
        # if data.status_code != 200:
        #     return {}
        
        # text = data.json()['text']

    return {'text': text, 'model': model}

    
class RelatedWordsView(Resource):
    def post(self):
        args = parser_related_words.parse_args()

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']

        # corpus_id = args['corpus_id']
        # model_id = args['model_id']
        # text = args['raw_text']
        # should_clean = args['clean_doc']
        # topn = args['topn']
        # use_ngram = args['use_ngram']
        
        # model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        # if model is None:
        #     return {}
        
        # # Clean document first.
        # if should_clean:
        #     text = clean_text(text)
        #     if not use_ngram:
        #         text = text.get('text')
        #     else:
        #         text = text.get('ngram_text', text.get('text'))
        #     # data = requests.post(cleaning_url, data=json.dumps({'raw_text': text}), headers=headers)
        #     # if data.status_code != 200:
        #     #     return {}
            
        #     # text = data.json()['text']

        return pd.read_json(
            model.get_similar_words(text, serialize=True)
        ).to_dict('records')

    def get(self):
        return self.post()
    
    
class RelatedDocsView(Resource):
    def post(self):
        print('Files: ', request.files)
        print('Form: ', request.form)
        print('Args: ', request.args)
        print('Values: ', request.values)

        args = parser_related_words.parse_args()
        # args['file'] = request.form['file']

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']

        # corpus_id = args['corpus_id']
        # model_id = args['model_id']
        # should_clean = args['clean_doc']
        # topn = args['topn']
        # use_ngram = args['use_ngram']

        # if 'file' in args:
        #     file = args['file']
        #     text = file.read()
        # elif 'raw_text' in args:
        #     text = args['raw_text']
        # else:
        #     return {'Error': 'Please provide a file or a raw_text parameter.'}

        # model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        # if model is None:
        #     return {'Error': f'No model found for {corpus_id}-{model_id}'}
        
        # # Clean document first.
        # if should_clean:
        #     text = clean_text(text)
        #     if not use_ngram:
        #         text = text.get('text')
        #     else:
        #         text = text.get('ngram_text', text.get('text'))
        #     # data = requests.post(cleaning_url, data=json.dumps({'raw_text': text}), headers=headers)
        #     # if data.status_code != 200:
        #     #     return {}
            
        #     # text = data.json()['text']

        payload = pd.read_json(
            model.get_similar_documents(text, serialize=True)
        ).to_dict('records')

        ids = [p['id'] for p in sorted(payload, key=lambda x: x['rank'])]
        for ix, m in enumerate(get_documents_metadata(ids)):
            payload[ix]['metadata'] = m

        return payload

    def get(self):
        return self.post()


# parser_by_id = reqparse.RequestParser()
# parser_by_id.add_argument(
#     'id', type=str,
#     required=True, help='Valid id of document in corpus.'
# )
# parser_by_id.add_argument(
#     'topn', type=int,
#     required=True, help='Number of similar docs to return.'
# )
# parser_by_id.add_argument(
#     'corpus_id', type=str,
#     required=True, help='Corpus used to train the word2vec model.'
# )
# parser_by_id.add_argument(
#     'model_id', type=str,
#     required=True, help='Identification for the model defined by the corpus partition and vector dimension.'
# )
# parser_by_id.add_argument(
#     'clean_doc', type=boolean,
#     required=True, help='Specifies whether cleaning should be done on the raw_text.'
# )
# parser_by_id.add_argument(
#     'use_ngram', type=boolean,
#     required=False, help='Flag to choose if ngram transformed text will be used.'
# )

# class RelatedDocsByIDView(Resource):
#     def post(self):
#         args = parser_related_words.parse_args()

#         corpus_id = args['corpus_id']
#         model_id = args['model_id']
#         id = args['id']
#         topn = args['topn']
        
#         model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
#         if model is None:
#             return {}
        
#         # Clean document first.
#         if should_clean:
#             text = clean_text(text)
#             if not use_ngram:
#                 text = text.get('text')
#             else:
#                 text = text.get('ngram_text', text.get('text'))
#             # data = requests.post(cleaning_url, data=json.dumps({'raw_text': text}), headers=headers)
#             # if data.status_code != 200:
#             #     return {}
            
#             # text = data.json()['text']

#         payload = pd.read_json(
#             model.get_similar_documents(text, serialize=True)
#         ).to_dict('records')

#         ids = [p['id'] for p in sorted(payload, key=lambda x: x['rank'])]
#         for ix, m in enumerate(get_documents_metadata(ids)):
#             payload[ix]['metadata'] = m

#         return payload

#     def get(self):
#         return self.post()

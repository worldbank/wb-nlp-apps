from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
import path_manager as pm
import os

parser = reqparse.RequestParser()
parser.add_argument(
    'corpus_id', type=str,
    required=True, help='ID for the corpus.'
)
parser.add_argument(
    'doc_id', type=str,
    required=True, help='ID of the document in the corpus.'
)
parser.add_argument(
    'is_cleaned', type=boolean, default=False,
    required=False, help='Flag indicating which text version to use.'
)


class FetchText(Resource):
    def post(self):
        args = parser.parse_args()
        corpus_id = args['corpus_id']
        doc_id = args['doc_id']
        is_cleaned = args['is_cleaned']

        if is_cleaned:
        	corpus_path = pm.get_txt_clean_path(corpus_id)
        else:
        	corpus_path = pm.get_txt_orig_path(corpus_id)
        
        file_path = os.path.join(corpus_path, f'{doc_id}.txt')
        if os.path.isfile(file_path):
        	try:
        		with open(file_path) as fl:
        			text = fl.read()
        	except:
        		with open(file_path, 'rb') as fl:
        			text = fl.read().decode('utf-8', 'ignore')

        else:
        	return {'Error': 'File not found.'}

        return {'text': text}

    def get(self):
        return self.post()

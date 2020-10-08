from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
import os

from wb_nlp.dir_manager import get_txt_data_dir

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
            corpus_path = get_txt_data_dir(corpus_id, text_type='CLEAN')
        else:
            corpus_path = get_txt_data_dir(corpus_id, text_type='ORIG')

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

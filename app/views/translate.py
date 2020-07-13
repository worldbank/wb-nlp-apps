from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean

from services.translation import translate


parser = reqparse.RequestParser()
parser.add_argument(
    'raw_text', type=str,
    required=True, help='raw text input required'
)
parser.add_argument(
    'src', type=str, default='auto',
    required=False, help='source language'
)
parser.add_argument(
    'dest', type=str, default='en',
    required=False, help='target language'
)
parser.add_argument(
    'with_extra_data', type=boolean, default=False,
    required=False, help='return more data'
)


class TranslateText(Resource):
    def post(self):
        args = parser.parse_args()
        text = args['raw_text']
        src = args['src']
        dest = args['dest']
        with_extra_data = args['with_extra_data']

        return translate(text=text, src=src, dest=dest, with_extra_data=with_extra_data)

    def get(self):
        return self.post()

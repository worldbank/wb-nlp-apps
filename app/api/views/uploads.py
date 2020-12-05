from flask_restful import Resource, reqparse
import werkzeug


parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files'
    required=True, help='File to upload.'
)

class UploadFile(Resource):
    def post(self):
        args = parser.parse_args()
        file = args['file']

        file.save('/')


class CleanText(Resource):
    def post(self):
        args = parser.parse_args()
        text = args['raw_text']
        
        return clean_text(text)

    def get(self):
        return self.post()

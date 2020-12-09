
from flask_restful import Resource


class EmptyAPI(Resource):
    def post(self):

        return {}

    def get(self):
        return self.post()

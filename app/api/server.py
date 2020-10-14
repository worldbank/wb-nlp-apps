from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from views.cleaning import CleanText
from views.word2vec import Word2VecView, RelatedWordsView, RelatedDocsView, RelatedDocsByIDView
from views.lda import (
    LDAModelInferTopics,
    LDARelatedDocsByIDView, LDARelatedDocsView, LDADocTopicsView,
    LDATopicWordsView, LDADocTopicsByIDView, LDAPartitionTopicShare,
    LDAModelTopicsView, LDATopicCompositionRangesView,
    LDADocsByTopicCompositionView,
)
from views.models import ModelsList
from views.text import FetchText
from views.translate import TranslateText
from views.upfile import EmptyAPI
import os
import sys

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

api = Api(app)

api.add_resource(CleanText, '/api/clean_text')
api.add_resource(EmptyAPI, '/api/empty')

api.add_resource(ModelsList, '/api/get_models')

api.add_resource(Word2VecView, '/api/word2vec')
api.add_resource(RelatedWordsView, '/api/related_words')
api.add_resource(RelatedDocsView, '/api/related_docs')
api.add_resource(RelatedDocsByIDView, '/api/related_docs_by_id')

api.add_resource(LDAModelInferTopics, '/api/lda_infer_topics')
api.add_resource(LDARelatedDocsView, '/api/lda_related_docs')
api.add_resource(LDARelatedDocsByIDView, '/api/lda_related_docs_by_id')
api.add_resource(LDADocTopicsByIDView, '/api/lda_doc_topics_by_id')
api.add_resource(LDADocTopicsView, '/api/lda_doc_topics')

api.add_resource(LDAModelTopicsView, '/api/get_lda_model_topics')
api.add_resource(LDAPartitionTopicShare,
                 '/api/lda_compare_partition_topic_share')

api.add_resource(LDATopicCompositionRangesView,
                 '/api/lda_topic_composition_ranges')
api.add_resource(LDADocsByTopicCompositionView,
                 '/api/lda_docs_by_topic_composition')

api.add_resource(FetchText, '/api/fetch_text')

api.add_resource(TranslateText, '/api/translate')

print('Server running...')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 8910

    # gunicorn -w 4 -b 0.0.0.0:8910 server:app
    # ss -lptn 'sport = :8910'
    app.run(host="0.0.0.0", debug=True, port=port)

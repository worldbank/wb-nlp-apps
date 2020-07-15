from path_manager import get_models_path
from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
import os
import json

import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.wrappers import LdaMallet

from sklearn.metrics import euclidean_distances

class CountryModule:
    def __init__(
        self, corpus_id, model_id
    ):
        # We will use the 0 index convention
        CORPUS_ID = corpus_id
        MODEL_ID = model_id

        self.corpus_id = corpus_id
        self.model_id = model_id

        self.corpus_part = '_'.join(model_id.split('_')[:-1])
        self.num_topics = int(model_id.split('_')[-1])

        self.models_path = get_models_path('LDA')
        self.model_folder = os.path.join(self.models_path, f'{CORPUS_ID}-{MODEL_ID}')

        self.normalized_topics = self.model.get_topics()
        self.topics = self.model.word_topics

        self.documents_topics = pd.read_csv(
            os.path.join(self.model_data_folder, f'doc_topics_{MODEL_ID}_with_details.csv'),
#             header='',  # Change to True if topic id should be present as the header
            index_col=0  # Change to True if the uid should be present as the index
        )

        self.documents_topics.columns = self.documents_topics.columns.astype(int)

        self.normalized_topics_by_documents = self.documents_topics / self.documents_topics.sum()
        self.normalized_documents_topics = self.documents_topics.div(self.documents_topics.sum(axis=1), axis=0)

        self.topic_composition_ranges = self._get_topic_composition_ranges()

    def get_docs_by_country_composition(self, topic_percentage, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):
        '''
        topic_percentage (dict): key (int) corresponds to topic id and value (float [0, 1]) corresponds to the expected topic percentage.
        '''
        topic_percentage = pd.Series(topic_percentage)

        candidate_docs = (self.normalized_documents_topics[topic_percentage.index] > topic_percentage).sum(axis=1)
        candidate_docs = candidate_docs[candidate_docs > 0]
        candidate_docs = self.normalized_documents_topics.loc[candidate_docs.index, topic_percentage.index].copy()

        if candidate_docs.empty:
            return []

        distance = euclidean_distances(topic_percentage.values.reshape(1, -1), candidate_docs)  # Note: transforming using .values may implicitly cause errors if the expected order of the index is not preserved.

        candidate_docs['score'] = distance[0]
        candidate_docs = candidate_docs.sort_values('score', ascending=True)
        candidate_docs = candidate_docs.reset_index()  # Since the index corresponds to the document id, then use .reset_index to convert it to a column
        candidate_docs.index.name = 'rank'
        candidate_docs = candidate_docs.reset_index()  # hax to define the rank
        candidate_docs['rank'] += 1
        candidate_docs['topic'] = candidate_docs[topic_percentage.index].to_dict('records')

        cols = ['id', 'rank', 'score', 'topic']
        payload = candidate_docs[cols].head(topn).to_dict('records')

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def _get_topic_composition_ranges(self):
        composition_range = pd.DataFrame(index=self.normalized_documents_topics.columns)
        composition_range.index.name = 'topic'

        composition_range['min'] = self.normalized_documents_topics.min()
        composition_range['max'] = self.normalized_documents_topics.max()

        payload = composition_range.reset_index().to_dict('records')

        return payload

    def get_topic_composition_ranges(self, serialize=False):
        payload = self.topic_composition_ranges

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

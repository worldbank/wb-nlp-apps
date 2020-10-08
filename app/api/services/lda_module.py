from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
import os
import json

import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.wrappers import LdaMallet

from sklearn.metrics import euclidean_distances
from wb_nlp.dir_manager import get_model_dir


class LDAInferencer:
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

        self.models_path = get_model_dir('LDA')
        self.model_folder = os.path.join(
            self.models_path, f'{CORPUS_ID}-{MODEL_ID}')

        self.model_data_folder = os.path.join(self.model_folder, 'data')

        self.model = LdaMallet.load(os.path.join(
            self.model_data_folder, f'{CORPUS_ID}_lda_model_{MODEL_ID}.mallet.lda'))
        self.gensim_model = malletmodel2ldamodel(
            self.model, iterations=self.model.iterations)

        self.g_dict = Dictionary()
        self.g_dict.id2token = self.model.id2word
        self.g_dict.token2id = {k: v for v, k in self.g_dict.id2token.items()}

        self.normalized_topics = self.model.get_topics()
        self.topics = self.model.word_topics

        self.documents_topics = pd.read_csv(
            os.path.join(self.model_data_folder,
                         f'doc_topics_{MODEL_ID}_with_details.csv'),
            #             header='',  # Change to True if topic id should be present as the header
            index_col=0  # Change to True if the uid should be present as the index
        )

        self.documents_topics.columns = self.documents_topics.columns.astype(
            int)

        self.normalized_topics_by_documents = self.documents_topics / \
            self.documents_topics.sum()
        self.normalized_documents_topics = self.documents_topics.div(
            self.documents_topics.sum(axis=1), axis=0)

        self.topic_composition_ranges = self._get_topic_composition_ranges()

    def get_topic_share(self, topic_id, doc_ids, serialize=False):
        if isinstance(doc_ids, str):
            doc_ids = [doc_ids]

        topic_share = self.normalized_topics_by_documents.reindex(doc_ids)[
            topic_id].to_dict()

        if serialize:
            topic_share = json.dumps(topic_share)

        return topic_share

    def infer_topics(self, text, topn_topics=None, total_topic_score=None, serialize=False):
        if isinstance(text, str):
            text = text.split()
        if len(text) == 1:
            doc_topics = self.gensim_model.get_term_topics(
                self.g_dict.token2id[text[0]])
        else:
            doc = self.g_dict.doc2bow(text)
            doc_topics = self.gensim_model[doc]

        found_topics = {i for i, v in doc_topics}
        print(found_topics)
        for i in range(self.model.num_topics):
            if i not in found_topics:
                doc_topics.append((i, 0))

        doc_topics = pd.DataFrame(doc_topics, columns=['topic', 'score'])
        doc_topics = doc_topics.sort_values('score', ascending=False)

        if total_topic_score is not None:
            tdoc_topics = doc_topics[doc_topics.score.cumsum(
            ) <= total_topic_score]
            if tdoc_topics.empty:
                doc_topics = doc_topics.head(1)
            else:
                doc_topics = tdoc_topics

        if topn_topics is not None and doc_topics.shape[0] > topn_topics:
            doc_topics = doc_topics.head(topn_topics)

        # doc_topics['topic'] = doc_topics['topic'].astype(int)
        doc_topics = doc_topics.to_dict('records')

        if serialize:
            doc_topics = json.dumps(doc_topics)

        return doc_topics

    def get_model_topic_words(self, topn_words=5, total_word_score=None, serialize=False):
        payload = []
        for topic_id in range(self.num_topics):
            topic_words = self.get_topic_words(
                topic_id,
                topn_words=topn_words,
                total_word_score=total_word_score
            )

            payload.append({'topic_id': topic_id, 'topic_words': topic_words})

        if serialize:
            payload = json.dumps(payload)

        return payload

    def get_topic_words(self, topic_id, topn_words=10, total_word_score=None, serialize=False):
        topic_id = int(topic_id)

        topic_words = pd.DataFrame(self.model.show_topic(
            topic_id, topn=topn_words), columns=['word', 'score'])
        topic_words = topic_words.sort_values('score', ascending=False)

        if total_word_score is not None:
            ttopic_words = topic_words[topic_words.score.cumsum(
            ) <= total_word_score]
            if ttopic_words.empty:
                topic_words = topic_words.head(1)
            else:
                topic_words = ttopic_words

        if topn_words is not None and topic_words.shape[0] > topn_words:
            topic_words = topic_words.head(topn_words)

        topic_words = topic_words.to_dict('records')

        if serialize:
            topic_words = json.dumps(topic_words)

        return topic_words

    def get_doc_topic_words(self, text, topn_topics=10, topn_words=10, total_topic_score=1, total_word_score=1, serialize=False):
        doc_topics = self.infer_topics(
            text, topn_topics=topn_topics, total_topic_score=total_topic_score)
        doc_topic_words = []
        for dt in doc_topics:
            topic = dt['topic']
            topic_score = dt['score']
            topic_words = self.get_topic_words(
                topic, topn_words=topn_words, total_word_score=total_word_score)

            topic_data = {'topic': topic, 'score': topic_score}
            topic_data['words'] = topic_words
            doc_topic_words.append(topic_data)

        doc_topic_words = pd.DataFrame(doc_topic_words).to_dict('records')

        if serialize:
            doc_topic_words = json.dumps(doc_topic_words)

        return doc_topic_words

    def get_doc_topic_words_by_id(self, doc_id, topn_topics=10, topn_words=10, total_topic_score=1, total_word_score=1, serialize=False):
        doc_topics = self.get_doc_topic_by_id(
            doc_id, topn=topn_topics, serialize=False)

        doc_topic_words = []
        for dt in doc_topics:
            topic = dt['topic']
            topic_score = dt['score']
            topic_words = self.get_topic_words(
                topic, topn_words=topn_words, total_word_score=total_word_score)

            topic_data = {'topic': topic, 'score': topic_score}
            topic_data['words'] = topic_words
            doc_topic_words.append(topic_data)

        doc_topic_words = pd.DataFrame(doc_topic_words).to_dict('records')

        if serialize:
            doc_topic_words = json.dumps(doc_topic_words)

        return doc_topic_words

    def get_combined_doc_topic_words(self, text, topn_topics=None, topn_words=None, total_topic_score=0.8, total_word_score=0.2, serialize=False):
        doc_topics = self.infer_topics(
            text, topn_topics=topn_topics, total_topic_score=total_topic_score)
        doc_topic_words = []
        for dt in doc_topics:
            topic = dt['topic']
            topic_score = dt['score']

            topic_words = self.get_topic_words(
                topic, topn_words=topn_words, total_word_score=total_word_score)
            for tw in topic_words:
                word = tw['word']
                word_score = tw['score']

                doc_topic_words.append({
                    'topic': topic,
                    'word': word,
                    'topic_score': topic_score,
                    'word_score': word_score,
                    'score': topic_score * word_score
                })

        doc_topic_words = pd.DataFrame(doc_topic_words).sort_values(
            'score', ascending=False).to_dict('records')

        if serialize:
            doc_topic_words = json.dumps(doc_topic_words)

        return doc_topic_words

    def get_doc_topic_by_id(self, doc_id, topn=None, serialize=False):
        doc = self.documents_topics.loc[doc_id]
        if doc.empty:
            return []

        # Just call is score for consistency
        doc.name = 'score'
        doc.index.name = 'topic'

        doc = doc.sort_values(ascending=False) / doc.sum()
        doc.index = doc.index.astype(int)

        doc = doc.reset_index()

        if topn is not None:
            doc = doc.head(topn)

        doc = doc.to_dict('records')

        if serialize:
            doc = json.dumps(doc)

        return doc

    def get_similar_documents(self, document, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):

        doc_topics = self.infer_topics(document)
        doc_topics = pd.DataFrame(doc_topics).sort_values(
            'topic').set_index('topic')

        e_distance = euclidean_distances(doc_topics.score.values.reshape(
            1, -1), self.normalized_documents_topics.values).flatten()

        if not show_duplicates:
            e_distance[e_distance <= duplicate_threshold] = np.inf

        payload = []
        for rank, top_sim_ix in enumerate(e_distance.argsort()[:topn], 1):
            payload.append(
                {'id': self.normalized_documents_topics.iloc[top_sim_ix].name, 'score': e_distance[top_sim_ix], 'rank': rank})

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_docs_by_id(self, doc_id, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):
        doc_topics = self.normalized_documents_topics.loc[doc_id].values.reshape(
            1, -1)

        e_distance = euclidean_distances(
            doc_topics, self.normalized_documents_topics.values).flatten()

        if not show_duplicates:
            e_distance[e_distance <= duplicate_threshold] = pd.np.inf

        payload = []
        for rank, top_sim_ix in enumerate(e_distance.argsort()[:topn], 1):
            payload.append(
                {'id': self.normalized_documents_topics.iloc[top_sim_ix].name, 'score': e_distance[top_sim_ix], 'rank': rank})

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_docs_by_topic_composition(self, topic_percentage, topn=10, return_data='id', closest_to_minimum=False, return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):
        '''
        topic_percentage (dict): key (int) corresponds to topic id and value (float [0, 1]) corresponds to the expected topic percentage.
        '''
        topic_percentage = pd.Series(topic_percentage)
        # Just in case we set the default values to zero
        topic_percentage = topic_percentage[topic_percentage > 0]

        candidate_docs = self.normalized_documents_topics[topic_percentage.index]
        candidate_docs = candidate_docs[
            (candidate_docs > topic_percentage).all(axis=1)
        ].copy()

        total_found = candidate_docs.shape[0]

        if total_found == 0:
            return {'total_found': total_found, 'payload': {}}

        # Note: transforming using .values may implicitly cause errors if the expected order of the index is not preserved.
        distance = euclidean_distances(
            topic_percentage.values.reshape(1, -1), candidate_docs)

        candidate_docs['score'] = distance[0]
        # Set to ascending=False if we want to show documents with higher topic composition than the given minimum. Use ascending=False if we want to get the documents with topic composition closest to the given minimum.
        candidate_docs = candidate_docs.sort_values(
            'score', ascending=closest_to_minimum)
        # Since the index corresponds to the document id, then use .reset_index to convert it to a column
        candidate_docs = candidate_docs.reset_index()
        candidate_docs.index.name = 'rank'
        candidate_docs = candidate_docs.reset_index()  # hax to define the rank
        candidate_docs['rank'] += 1
        candidate_docs['topic'] = candidate_docs[topic_percentage.index].to_dict(
            'records')

        cols = ['id', 'rank', 'score', 'topic']
        payload = candidate_docs[cols].head(topn).to_dict('records')

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return {'total_found': total_found, 'payload': payload}

    def _get_topic_composition_ranges(self):
        composition_range = pd.DataFrame(
            index=self.normalized_documents_topics.columns)
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

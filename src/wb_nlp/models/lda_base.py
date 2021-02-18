'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import json
import logging
import pandas as pd
from gensim.models.ldamulticore import LdaMulticore

import numpy as np

from wb_nlp.interfaces.milvus import (
    get_milvus_client, get_embedding_dsl
)

from wb_nlp.types.models import LDAModelConfig, ModelTypes
from wb_nlp.utils.scripts import (
    configure_logger,
)
from wb_nlp.models.base import BaseModel


class LDAModel(BaseModel):
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class=LdaMulticore,
        model_config_type=LDAModelConfig,
        expected_model_name=ModelTypes.lda.value,
        raise_empty_doc_status=True,
        log_level=logging.WARNING,
    ):
        configure_logger(log_level)
        self.log_level = log_level
        self.logger = logging.getLogger(__file__)

        self.cleaning_config_id = cleaning_config_id
        self.model_config_id = model_config_id
        self.model_class = model_class  # Example: LdaMulticore
        self.model_config_type = model_config_type  # Example: LDAModelConfig
        self.expected_model_name = expected_model_name

        self.validate_and_prepare_requirements()

        self.model = None
        self.raise_empty_doc_status = raise_empty_doc_status

        # Try to load the model
        self.load()
        self.set_model_specific_attributes()

        self.create_milvus_collection()

    def set_model_specific_attributes(self):
        self.num_topics = self.dim

    def transform_doc(self, document, normalize=True, tolist=False):
        # This function is the primary method of converting a document
        # into its vector representation based on the model.
        # This should be implemented in the respective models.
        # The expected output is a dictionary with keys:
        # - doc_vec  # numpy array of shape (1, self.dim)
        # - success  # Whether the transformation went successfully
        self.check_model()
        success = True

        try:

            doc_topics = self.infer_topics(document)
            doc_vec = np.array([dt["score"] for dt in sorted(
                doc_topics, key=lambda x: x["topic"])]).reshape(1, -1)

            if normalize:
                doc_vec /= np.linalg.norm(doc_vec, ord=2)

        except Exception as e:
            success = False
            if self.raise_empty_doc_status:
                raise(e)
            else:
                doc_vec = np.zeros(self.dim).reshape(1, -1)

        if tolist:
            doc_vec = doc_vec.ravel().tolist()

        return dict(doc_vec=doc_vec, success=success)

    def infer_topics(self, text, topn_topics=None, total_topic_score=None, serialize=False):
        if isinstance(text, str):
            text = text.split()
        if len(text) == 1:
            doc_topics = self.model.get_term_topics(
                self.g_dict.token2id[text[0]])
        else:
            doc = self.g_dict.doc2bow(text)
            doc_topics = self.model[doc]

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
        for topic_id in range(self.model.num_topics):
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

    # def get_doc_topic_words_by_id(self, doc_id, topn_topics=10, topn_words=10, total_topic_score=1, total_word_score=1, serialize=False):
    #     doc_topics = self.get_doc_topic_by_id(
    #         doc_id, topn=topn_topics, serialize=False)

    #     doc_topic_words = []
    #     for dt in doc_topics:
    #         topic = dt['topic']
    #         topic_score = dt['score']
    #         topic_words = self.get_topic_words(
    #             topic, topn_words=topn_words, total_word_score=total_word_score)

    #         topic_data = {'topic': topic, 'score': topic_score}
    #         topic_data['words'] = topic_words
    #         doc_topic_words.append(topic_data)

    #     doc_topic_words = pd.DataFrame(doc_topic_words).to_dict('records')

    #     if serialize:
    #         doc_topic_words = json.dumps(doc_topic_words)

    #     return doc_topic_words

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

    # def get_doc_topic_by_id(self, doc_id, topn=None, serialize=False):
    #     doc = self.documents_topics.loc[doc_id]
    #     if doc.empty:
    #         return []

    #     # Just call is score for consistency
    #     doc.name = 'score'
    #     doc.index.name = 'topic'

    #     doc = doc.sort_values(ascending=False) / doc.sum()
    #     doc.index = doc.index.astype(int)

    #     doc = doc.reset_index()

    #     if topn is not None:
    #         doc = doc.head(topn)

    #     doc = doc.to_dict('records')

    #     if serialize:
    #         doc = json.dumps(doc)

    #     return doc

    # def get_similar_documents(self, document, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):

    #     doc_topics = self.infer_topics(document)
    #     doc_topics = pd.DataFrame(doc_topics).sort_values(
    #         'topic').set_index('topic')

    #     e_distance = euclidean_distances(doc_topics.score.values.reshape(
    #         1, -1), self.normalized_documents_topics.values).flatten()

    #     if not show_duplicates:
    #         e_distance[e_distance <= duplicate_threshold] = np.inf

    #     payload = []
    #     for rank, top_sim_ix in enumerate(e_distance.argsort()[:topn], 1):
    #         payload.append(
    #             {'id': self.normalized_documents_topics.iloc[top_sim_ix].name, 'score': e_distance[top_sim_ix], 'rank': rank})

    #     if serialize:
    #         payload = pd.DataFrame(payload).to_json()

    #     return payload

    # def get_similar_docs_by_id(self, doc_id, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):
    #     doc_topics = self.normalized_documents_topics.loc[doc_id].values.reshape(
    #         1, -1)

    #     e_distance = euclidean_distances(
    #         doc_topics, self.normalized_documents_topics.values).flatten()

    #     if not show_duplicates:
    #         e_distance[e_distance <= duplicate_threshold] = pd.np.inf

    #     payload = []
    #     for rank, top_sim_ix in enumerate(e_distance.argsort()[:topn], 1):
    #         payload.append(
    #             {'id': self.normalized_documents_topics.iloc[top_sim_ix].name, 'score': e_distance[top_sim_ix], 'rank': rank})

    #     if serialize:
    #         payload = pd.DataFrame(payload).to_json()

    #     return payload

    def get_docs_by_topic_composition(self, topic_percentage, topn=10, closest_to_minimum=False, serialize=False, from_result=0, size=10, show_duplicates=False, duplicate_threshold=0.98, metric_type="IP"):
        '''
        topic_percentage (dict): key (int) corresponds to topic id and value (float [0, 1]) corresponds to the expected topic percentage.
        '''
        self.check_wvecs()

        topic_filter_vec = np.array(
            [topic_percentage.get(i, 0) for i in range(self.dim)])

        topk = 2 * size  # Add buffer
        dsl = get_embedding_dsl(
            topic_filter_vec, topk, vector_field_name=self.milvus_vector_field_name, metric_type=metric_type)
        results = get_milvus_client().search(self.model_collection_id, dsl)

        entities = results[0]
        payload = []

        for rank, ent in enumerate(entities):

            if from_result > rank:
                continue

            if not show_duplicates:
                # TODO: Make sure that this is true for Milvus.
                # If we change the metric_type, this should be adjusted somehow.
                if ent.distance > duplicate_threshold:
                    continue

            payload.append({'id': self.get_doc_id_from_int_id(ent.id), 'score': float(np.round(
                ent.distance, decimals=5)), 'rank': rank + 1})

            if len(payload) == size:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

        # candidate_docs = self.normalized_documents_topics[topic_percentage.index]
        # candidate_docs = candidate_docs[
        #     (candidate_docs > topic_percentage).all(axis=1)
        # ].copy()

        # total_found = candidate_docs.shape[0]

        # if total_found == 0:
        #     return {'total_found': total_found, 'payload': {}}

        # # Note: transforming using .values may implicitly cause errors if the expected order of the index is not preserved.
        # distance = euclidean_distances(
        #     topic_percentage.values.reshape(1, -1), candidate_docs)

        # candidate_docs['score'] = distance[0]
        # # Set to ascending=False if we want to show documents with higher topic composition than the given minimum. Use ascending=False if we want to get the documents with topic composition closest to the given minimum.
        # candidate_docs = candidate_docs.sort_values(
        #     'score', ascending=closest_to_minimum)
        # # Since the index corresponds to the document id, then use .reset_index to convert it to a column
        # candidate_docs = candidate_docs.reset_index()
        # candidate_docs.index.name = 'rank'
        # candidate_docs = candidate_docs.reset_index()  # hax to define the rank
        # candidate_docs['rank'] += 1
        # candidate_docs['topic'] = candidate_docs[topic_percentage.index].to_dict(
        #     'records')

        # cols = ['id', 'rank', 'score', 'topic']
        # payload = candidate_docs[cols].head(topn).to_dict('records')

        # if serialize:
        #     payload = pd.DataFrame(payload).to_json()

        # return {'total_found': total_found, 'payload': payload}

    # def _get_topic_composition_ranges(self):
    #     composition_range = pd.DataFrame(
    #         index=self.normalized_documents_topics.columns)
    #     composition_range.index.name = 'topic'

    #     composition_range['min'] = self.normalized_documents_topics.min()
    #     composition_range['max'] = self.normalized_documents_topics.max()

    #     payload = composition_range.reset_index().to_dict('records')

    #     return payload
    # def get_topic_composition_ranges(self, serialize=False):
    #     payload = self.topic_composition_ranges
    #     if serialize:
    #         payload = pd.DataFrame(payload).to_json()
    #     return payload
if __name__ == '__main__':
    """
    import glob
    from pathlib import Path
    import hashlib
    import pandas as pd

    from wb_nlp.models.word2vec import word2vec

    doc_fnames = list(Path('./data/raw/sample_data/TXT_ORIG').glob('*.txt'))
    doc_ids = [hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15] for p in doc_fnames]
    corpus = ['WB'] * len(doc_ids)

    doc_df = pd.DataFrame()
    doc_df['id'] = doc_ids
    doc_df['corpus'] = corpus
    doc_df['text'] = [open(fn, 'rb').read().decode('utf-8', errors='ignore') for fn in doc_fnames]

    wvec_model = word2vec.Word2VecModel(corpus_id='WB', model_id='ALL_50', cleaning_config_id='cid', doc_df=doc_df, model_path='./models/', iter=10)
    %time wvec_model.train_model()

    wvec_model.build_doc_vecs(pool_workers=3)
    wvec_model.get_similar_words('bank')
    wvec_model.get_similar_documents('bank')
    wvec_model.get_similar_docs_by_id(doc_id='8314385c25c7c5e')
    wvec_model.get_similar_words_by_id(doc_id='8314385c25c7c5e')
    """
    import logging
    from wb_nlp.models import lda_base

    # rm data/corpus/cleaned/23f78350192d924e4a8f75278aca0e1c/bow_corpus-531c1e4f358efbc07b97a58815558c53_5a80eb483f11c3b899d8cba7237215f9.mm*
    # rm data/corpus/cleaned/23f78350192d924e4a8f75278aca0e1c/dictionary-531c1e4f358efbc07b97a58815558c53_5a80eb483f11c3b899d8cba7237215f9.gensim.dict
    # rm -rf models/lda/5ac7fd8a83c6bc5fce480323eb01d137

    lda_model = lda_base.LDAModel(
        model_config_id="ef0ab0459e9c28de8657f3c4f5b2cd86",
        cleaning_config_id="23f78350192d924e4a8f75278aca0e1c",
        model_class=LdaMulticore,
        model_config_type=LDAModelConfig,
        expected_model_name="lda",
        raise_empty_doc_status=False, log_level=logging.DEBUG)
    # %time
    lda_model.train_model()
    # Do this if the model is available in disk but the model_run_info is not. This is to dump the model_run_info to db in case it's not present.
    # lda_model.save()

    lda_model.build_doc_vecs(pool_workers=3)
    print(lda_model.get_similar_words('bank'))
    print(lda_model.get_similar_documents('bank'))
    print(lda_model.get_similar_docs_by_doc_id(doc_id='wb_725385'))
    print(lda_model.get_similar_words_by_doc_id(doc_id='wb_725385'))

    # lda_model.drop_milvus_collection()

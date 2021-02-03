'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import gc
import json
import logging
from pathlib import Path
import pandas as pd
import gensim
from gensim.models.ldamulticore import LdaMulticore
from gensim.corpora import Dictionary, MmCorpus

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from joblib import Parallel, delayed

from milvus import DataType
from wb_nlp.interfaces.milvus import (
    get_milvus_client, get_hex_id, get_int_id,
    get_collection_ids, get_embedding_dsl,
)
from wb_nlp.interfaces import mongodb
from wb_nlp.utils.scripts import create_dask_cluster
from wb_nlp.types.models import LDAModelConfig, ModelRunInfo
from wb_nlp import dir_manager
from wb_nlp.processing.corpus import MultiDirGenerator
from wb_nlp.utils.scripts import (
    configure_logger,
    generate_model_hash,
    checkpoint_log,
    get_cleaned_corpus_id
)
from wb_nlp.models.base import BaseModel


class LDAModel(BaseModel):
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class,
        model_config_type,
        expected_model_name,
        raise_empty_doc_status=True,
        log_level=logging.WARNING,
    ):
        configure_logger(log_level)
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

    def transform_doc(self, document, normalize=True):
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

    # def get_docs_by_topic_composition(self, topic_percentage, topn=10, return_data='id', closest_to_minimum=False, return_similarity=False, duplicate_threshold=0.01, show_duplicates=True, serialize=False):
    #     '''
    #     topic_percentage (dict): key (int) corresponds to topic id and value (float [0, 1]) corresponds to the expected topic percentage.
    #     '''
    #     topic_percentage = pd.Series(topic_percentage)
    #     # Just in case we set the default values to zero
    #     topic_percentage = topic_percentage[topic_percentage > 0]

    #     candidate_docs = self.normalized_documents_topics[topic_percentage.index]
    #     candidate_docs = candidate_docs[
    #         (candidate_docs > topic_percentage).all(axis=1)
    #     ].copy()

    #     total_found = candidate_docs.shape[0]

    #     if total_found == 0:
    #         return {'total_found': total_found, 'payload': {}}

    #     # Note: transforming using .values may implicitly cause errors if the expected order of the index is not preserved.
    #     distance = euclidean_distances(
    #         topic_percentage.values.reshape(1, -1), candidate_docs)

    #     candidate_docs['score'] = distance[0]
    #     # Set to ascending=False if we want to show documents with higher topic composition than the given minimum. Use ascending=False if we want to get the documents with topic composition closest to the given minimum.
    #     candidate_docs = candidate_docs.sort_values(
    #         'score', ascending=closest_to_minimum)
    #     # Since the index corresponds to the document id, then use .reset_index to convert it to a column
    #     candidate_docs = candidate_docs.reset_index()
    #     candidate_docs.index.name = 'rank'
    #     candidate_docs = candidate_docs.reset_index()  # hax to define the rank
    #     candidate_docs['rank'] += 1
    #     candidate_docs['topic'] = candidate_docs[topic_percentage.index].to_dict(
    #         'records')

    #     cols = ['id', 'rank', 'score', 'topic']
    #     payload = candidate_docs[cols].head(topn).to_dict('records')

    #     if serialize:
    #         payload = pd.DataFrame(payload).to_json()

    #     return {'total_found': total_found, 'payload': payload}

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

    def combine_word_vectors(self, word_vecs):
        return word_vecs.mean(axis=0).reshape(1, -1)

    def transform_doc(self, document, normalize=True):
        # document: cleaned string

        self.check_model()
        success = True

        try:
            tokens = [i for i in document.split() if i in self.model.wv.vocab]
            word_vecs = self.model.wv[tokens]
            word_vecs = self.combine_word_vectors(word_vecs)

            if normalize:
                word_vecs /= np.linalg.norm(word_vecs, ord=2)

        except Exception as e:
            success = False
            if self.raise_empty_doc_status:
                raise(e)
            else:
                word_vecs = np.zeros(self.model.vector_size).reshape(1, -1)

        return dict(word_vecs=word_vecs, success=success)

    def process_doc(self, doc, normalize=True):
        text = doc.get('text')

        if not text:
            fname = self.cleaned_docs_dir / doc["corpus"] / f"{doc['id']}.txt"
            with open(fname, "rb") as open_file:
                text = open_file.read().decode("utf-8", errors="ignore")

        return self.transform_doc(text, normalize=normalize)

    def build_doc_vecs(self, pool_workers=None):
        # Input is a dataframe containing the following columns:
        # - text
        # - corpus (corpus code corresponding to which corpus the text came from)
        # - id (some hash value (max of 15-hex value) - we will convert this to its decimal equivalent)
        self.check_model()

        # docs_metadata_collection = mongodb.get_docs_metadata_collection()
        docs_metadata_collection = mongodb.get_collection(
            db_name="test_nlp", collection_name="docs_metadata")

        milvus_client = get_milvus_client()
        collection_name = self.model_collection_id

        if collection_name not in milvus_client.list_collections():
            milvus_client.create_collection(
                collection_name, self.collection_params)

        collection_doc_ids = set(get_collection_ids(collection_name))

        projection = ["id", "int_id", "hex_id", "corpus"]

        docs_metadata_df = pd.DataFrame(
            list(docs_metadata_collection.find(projection=projection)), columns=projection)

        docs_for_processing = docs_metadata_df[
            ~docs_metadata_df['int_id'].isin(collection_doc_ids)]

        dask_client = create_dask_cluster(
            logger=None, n_workers=pool_workers)

        try:
            with joblib.parallel_backend('dask'):
                for partition_group, sub_docs in docs_for_processing.groupby('corpus'):
                    results = Parallel(verbose=10, batch_size='auto')(
                        delayed(self.process_doc)(doc) for idx, doc in sub_docs.iterrows())

                    locs, vectors = list(zip(
                        *[(ix, p['word_vecs'].flatten()) for ix, p in enumerate(results) if p['success']]))
                    sub_int_ids = sub_docs.iloc[list(
                        locs)]['int_id'].tolist()

                    entities = [
                        {"name": self.milvus_vector_field_name, "values": vectors,
                            "type": DataType.FLOAT_VECTOR},
                    ]

                    if not milvus_client.has_partition(collection_name, partition_group):
                        milvus_client.create_partition(
                            collection_name, partition_group)

                    ids = milvus_client.insert(collection_name, entities,
                                               sub_int_ids, partition_tag=partition_group)

                    assert len(set(ids).difference(sub_int_ids)) == 0

                    milvus_client.flush([collection_name])
        finally:
            dask_client.close()

    def get_doc_vec(self, document, normalize=True, assert_success=True, flatten=True):
        doc_vec_payload = self.transform_doc(document, normalize=normalize)
        doc_vec = doc_vec_payload['word_vecs']

        if assert_success and not doc_vec_payload['success']:
            raise ValueError("Document was mapped to the zero vector!")

        return doc_vec.flatten() if flatten else doc_vec

    def get_similar_documents(self, document, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.98, show_duplicates=False, serialize=False):
        # document: any text
        # topn: number of returned related documents in the database
        # return_data: string corresponding to a column in the docs or list of column names
        # return_similarity: option if similarity scores are to be returned
        # duplicate_threhold: threshold that defines a duplicate document based on similarity score
        # show_duplicates: option if exact duplicates of documents are to be considered as return documents
        self.check_wvecs()

        doc_vec = self.get_doc_vec(
            document, normalize=True, assert_success=True, flatten=True)

        topk = 2 * topn  # Add buffer
        dsl = get_embedding_dsl(
            doc_vec, topk, vector_field_name=self.milvus_vector_field_name, metric_type="IP")
        results = get_milvus_client().search(self.model_collection_id, dsl)

        entities = results[0]
        payload = []

        for rank, ent in enumerate(entities, 1):
            if not show_duplicates:
                if ent.distance > duplicate_threshold:
                    continue

            hex_id = get_hex_id(ent.id)
            payload.append({'id': hex_id, 'score': np.round(
                ent.distance, decimals=5), 'rank': rank})

            if len(payload) == topn:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_words(self, document, topn=10, return_similarity=False, serialize=False):

        doc_vec = self.get_doc_vec(
            document, normalize=True, assert_success=True, flatten=False)

        sim = cosine_similarity(doc_vec, self.model.wv.vectors).flatten()

        payload = []
        for rank, top_sim_ix in enumerate(sim.argsort()[-topn:][::-1], 1):
            payload.append({'word': self.model.wv.index2word[top_sim_ix], 'score': np.round(
                sim[top_sim_ix], decimals=5), 'rank': rank})

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_docs_by_id(self, doc_id, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.98, show_duplicates=False, serialize=False):
        self.check_wvecs()

        int_id = get_int_id(doc_id)
        doc = get_milvus_client().get_entity_by_id(
            self.model_collection_id, ids=[int_id])[0]
        if doc is None:
            raise ValueError(
                f'Document id `{doc_id}` not found in the vector index `{self.model_collection_id}`.')

        doc_vec = np.array(doc.embedding)
        topk = 2 * topn
        dsl = get_embedding_dsl(doc_vec,
                                topk, vector_field_name=self.milvus_vector_field_name, metric_type="IP")
        results = get_milvus_client().search(self.model_collection_id, dsl)

        entities = results[0]
        payload = []

        for rank, ent in enumerate(entities, 1):
            if not show_duplicates:
                if ent.distance > duplicate_threshold:
                    continue

            hex_id = get_hex_id(ent.id)
            payload.append({'id': hex_id, 'score': np.round(
                ent.distance, decimals=5), 'rank': rank})

            if len(payload) == topn:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_words_by_id(self, doc_id, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.98, show_duplicates=False, serialize=False):
        self.check_wvecs()

        int_id = get_int_id(doc_id)
        doc = get_milvus_client().get_entity_by_id(
            self.model_collection_id, ids=[int_id])[0]
        if doc is None:
            raise ValueError(
                f'Document id `{doc_id}` not found in the vector index `{self.model_collection_id}`.')

        doc_vec = np.array(doc.embedding).reshape(1, -1)

        sim = cosine_similarity(doc_vec, self.model.wv.vectors).flatten()

        payload = []
        for rank, top_sim_ix in enumerate(sim.argsort()[-topn:][::-1], 1):
            payload.append({'word': self.model.wv.index2word[top_sim_ix], 'score': np.round(
                sim[top_sim_ix], decimals=5), 'rank': rank})

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def check_model(self):
        if self.model is None:
            raise ValueError('Model not trained!')

    def check_wvecs(self):
        collection_doc_ids = get_collection_ids(self.model_collection_id)

        if len(collection_doc_ids) == 0:
            raise ValueError('Document vectors not available!')

    # def rescue_code(self, function):
    #     # http://blog.rtwilson.com/how-to-rescue-lost-code-from-a-jupyteripython-notebook/
    #     import inspect
    #     get_ipython().set_next_input(
    #         "".join(inspect.getsourcelines(function)[0]))

    def augment_query(self):
        """Implements an augmented query using a pretrained
        word2vec model, e.g., wikipedia, in the event that a zero vector
        is generated.
        """
        pass


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

    # lda_model.build_doc_vecs(pool_workers=3)
    # print(lda_model.get_similar_words('bank'))
    # print(lda_model.get_similar_documents('bank'))
    # print(lda_model.get_similar_docs_by_id(doc_id='092d1961ab4f9a7'))
    # print(lda_model.get_similar_words_by_id(doc_id='092d1961ab4f9a7'))

    # print(wvec_model.get_similar_docs_by_id(doc_id='8314385c25c7c5e'))
    # print(wvec_model.get_similar_words_by_id(doc_id='8314385c25c7c5e'))

    milvus_client = get_milvus_client()
    collection_name = lda_model.model_collection_id

    if collection_name in milvus_client.list_collections():
        milvus_client.drop_collection(collection_name)

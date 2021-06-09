'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import gc
import os
import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from joblib import Parallel, delayed

from milvus import DataType
from wb_nlp.interfaces.milvus import (
    get_milvus_client, get_hex_id, get_int_id,
    get_collection_ids, get_embedding_dsl,
)

from wb_nlp.utils.scripts import create_dask_cluster


class Word2VecModel:
    def __init__(
        self,
        corpus_id,
        model_id,
        cleaning_config_id,
        doc_df=None,
        dim=100,
        window=10,
        negative=10,
        min_count=5,
        sg=1,
        workers=4,
        model_path='./',
        iter=10,
        raise_empty_doc_status=True
    ):
        self.cleaning_config_id = cleaning_config_id
        self.corpus_id = corpus_id
        self.model_id = model_id
        self.model = None
        self.workers = workers
        self.iter = iter
        self.dim = dim
        self.window = window
        self.negative = negative
        self.min_count = min_count
        self.sg = sg
        self.raise_empty_doc_status = raise_empty_doc_status

        self.model_path = model_path

        self.model_collection_id = f'word2vec_{self.model_id}'
        self.model_path = os.path.join(
            self.model_path, f'{self.model_collection_id}.mm')

        self.docs = doc_df.copy() if doc_df is not None else doc_df

        self.milvus_vector_field_name = "embedding"

        self.collection_params = {
            "fields": [
                {"name": self.milvus_vector_field_name, "type": DataType.FLOAT_VECTOR,
                    "params": {"dim": self.dim}},
            ],
            "segment_row_limit": 4096,
            "auto_id": False
        }

        milvus_client = get_milvus_client()

        if self.model_collection_id not in milvus_client.list_collections():
            milvus_client.create_collection(
                self.model_collection_id, self.collection_params)

    def clear(self):
        del(self.docs)
        del(self.model)

        self.docs = None
        self.model = None

        gc.collect()

    def save(self):
        self.save_model()

    def load(self):
        self.load_model()

        # Make sure that the dimensionality uses the one in the trained model.
        if self.dim != self.model.wv.vector_size:
            print(
                'Warning: dimension declared is not aligned with loaded model. Using loaded model dim.')
            self.dim = self.model.wv.vector_size

    def save_model(self):
        self.check_model()
        self.model.save(self.model_path)

    def load_model(self):
        self.model = Word2Vec.load(self.model_path)

    def train_model(self, retrain=False):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.

        if self.model is None or retrain:
            self.model = Word2Vec(
                self.docs.text.str.split().values,
                size=self.dim, min_count=self.min_count,
                workers=self.workers, iter=self.iter,
                window=self.window, negative=self.negative, sg=self.sg
            )

            milvus_client = get_milvus_client()
            collection_name = self.model_collection_id

            if collection_name in milvus_client.list_collections():
                milvus_client.drop_collection(collection_name)

        else:
            print('Warning: Model already trained. Not doing anything...')

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

    def build_doc_vecs(self, pool_workers=None):
        # Input is a dataframe containing the following columns:
        # - text
        # - corpus (corpus code corresponding to which corpus the text came from)
        # - id (some hash value (max of 15-hex value) - we will convert this to its decimal equivalent)
        self.check_model()

        milvus_client = get_milvus_client()
        collection_name = self.model_collection_id

        if collection_name not in milvus_client.list_collections():
            milvus_client.create_collection(
                collection_name, self.collection_params)

        ids = self.docs['id'].values

        collection_doc_ids = set(get_collection_ids(collection_name))

        int_ids = list(map(get_int_id, ids))
        self.docs['int_ids'] = int_ids

        ids_for_processing = {
            hid: iid for hid, iid in zip(ids, int_ids) if iid not in collection_doc_ids}

        docs = self.docs[self.docs['id'].isin(list(ids_for_processing))]

        dask_client = create_dask_cluster(logger=None, n_workers=pool_workers)

        try:
            with joblib.parallel_backend('dask'):
                for partition_group, sub_docs in docs.groupby('corpus'):
                    results = Parallel(verbose=10, batch_size='auto')(
                        delayed(self.transform_doc)(text) for text in sub_docs.text)

                    locs, vectors = list(zip(
                        *[(ix, p['word_vecs'].flatten()) for ix, p in enumerate(results) if p['success']]))
                    sub_int_ids = sub_docs.iloc[list(
                        locs)]['int_ids'].tolist()

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

    import glob
    from pathlib import Path
    import hashlib
    import pandas as pd

    from wb_nlp.models.word2vec import word2vec

    doc_fnames = list(Path('./data/raw/sample_data/TXT_ORIG').glob('*.txt'))
    doc_ids = [hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15]
               for p in doc_fnames]
    corpus = ['WB'] * len(doc_ids)

    doc_df = pd.DataFrame()
    doc_df['id'] = doc_ids
    doc_df['corpus'] = corpus
    doc_df['text'] = [open(fn, 'rb').read().decode(
        'utf-8', errors='ignore') for fn in doc_fnames]

    wvec_model = word2vec.Word2VecModel(
        corpus_id='WB', model_id='ALL_50', cleaning_config_id='cid', doc_df=doc_df, model_path='./models/', iter=10)
    # %time
    wvec_model.train_model()

    wvec_model.build_doc_vecs(pool_workers=3)
    print(wvec_model.get_similar_words('bank'))
    print(wvec_model.get_similar_documents('bank'))
    print(wvec_model.get_similar_docs_by_id(doc_id='8314385c25c7c5e'))
    print(wvec_model.get_similar_words_by_id(doc_id='8314385c25c7c5e'))

    milvus_client = get_milvus_client()
    collection_name = wvec_model.model_collection_id

    if collection_name in milvus_client.list_collections():
        milvus_client.drop_collection(collection_name)
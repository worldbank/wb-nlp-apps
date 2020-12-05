import os
import pandas as pd
from gensim.models import Word2Vec
import numpy as np
import multiprocessing as mp
import gc
from sklearn.metrics.pairwise import cosine_similarity


class Word2VecModel:
    def __init__(
        self,
        corpus_id,
        model_id,
        doc_df=None,
        dim=100,
        window=10,
        negative=10,
        min_count=5,
        sg=1,
        workers=4,
        model_path='./',
        optimize_interval=0,
        iter=10,
        raise_empty_doc_status=True
    ):
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

        self.model_data_id = f'{self.corpus_id.lower()}-w2vec_{self.model_id}'
        self.vecs_path = os.path.join(
            self.model_path, f'{self.model_data_id}.hdf')
        self.model_path = os.path.join(
            self.model_path, f'{self.model_data_id}.mm')

        self.vecs = None
        self.docs = doc_df.copy() if doc_df is not None else doc_df

    def clear(self):
        del(self.vecs)
        del(self.docs)
        del(self.model)

        self.vecs = None
        self.docs = None
        self.model = None

        gc.collect()

    def save(self):
        self.save_model()
        self.save_vecs()

    def load(self):
        self.load_vecs()
        self.load_model()

        # Make sure that the dimensionality uses the one in the trained model.
        if self.dim != self.model.wv.vector_size:
            print(
                'Warning: dimension declared is not aligned with loaded model. Using loaded model dim.')
            self.dim = self.model.wv.vector_size

    def save_vecs(self):
        self.check_wvecs()
        self.vecs.to_hdf(self.vecs_path, 'vecs')

    def save_model(self):
        self.check_model()
        self.model.save(self.model_path)

    def load_model(self):
        self.model = Word2Vec.load(self.model_path)

    def load_vecs(self):
        self.vecs = pd.read_hdf(self.vecs_path, 'vecs')

    def train_model(self):
        if self.model is None:
            self.model = Word2Vec(
                self.docs.text.str.split().values,
                size=self.dim, min_count=self.min_count,
                workers=self.workers, iter=self.iter,
                window=self.window, negative=self.negative, sg=self.sg
            )
        else:
            print('Warning: Model already trained. Not doing anything...')

    def transform_doc(self, document):
        # document: cleaned string

        self.check_model()

        try:
            tokens = [i for i in document.split() if i in self.model.wv.vocab]
            word_vecs = self.model.wv[tokens]
            word_vecs = word_vecs.mean(axis=0).reshape(1, -1)

        except Exception as e:
            if self.raise_empty_doc_status:
                raise(e)
            else:
                word_vecs = np.zeros(self.model.vector_size).reshape(1, -1)

        return word_vecs

    def build_doc_vecs(self, pool_workers=None):
        self.vecs = self.docs[['id']]

        if pool_workers is None:
            self.vecs['wvecs'] = self.docs.text.map(self.transform_doc)
        else:
            pool = mp.Pool(processes=pool_workers)
            self.vecs['wvecs'] = pool.map(self.transform_doc, self.docs.text)
            pool.close()
            pool.join()

#         if self.docs.index.max() != (self.docs.shape[0] - 1):
#             self.docs = self.docs.reset_index(drop='index')

        if self.vecs.index.max() != (self.vecs.shape[0] - 1):
            self.vecs = self.vecs.reset_index(drop='index')

    def get_similar_documents(self, document, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.98, show_duplicates=False, serialize=False):
        # document: any text
        # topn: number of returned related documents in the database
        # return_data: string corresponding to a column in the docs or list of column names
        # return_similarity: option if similarity scores are to be returned
        # duplicate_threhold: threshold that defines a duplicate document based on similarity score
        # show_duplicates: option if exact duplicates of documents are to be considered as return documents
        self.check_wvecs()

        doc_vec = self.transform_doc(document)

        sim = cosine_similarity(doc_vec, np.vstack(self.vecs.wvecs)).flatten()

        if not show_duplicates:
            sim[sim > duplicate_threshold] = 0

        payload = []
        for rank, top_sim_ix in enumerate(sim.argsort()[-topn:][::-1], 1):
            payload.append({'id': self.vecs.iloc[top_sim_ix][return_data], 'score': np.round(
                sim[top_sim_ix], decimals=5), 'rank': rank})

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_words(self, document, topn=10, return_similarity=False, serialize=False):

        doc_vec = self.transform_doc(document)
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
        doc_vec = np.array(
            self.vecs[self.vecs['id'] == doc_id]['wvecs'].iloc[0]).reshape(1, -1)

        sim = cosine_similarity(doc_vec, np.vstack(self.vecs.wvecs)).flatten()

        if not show_duplicates:
            sim[sim > duplicate_threshold] = 0

        payload = []
        for rank, top_sim_ix in enumerate(sim.argsort()[-topn:][::-1], 1):
            payload.append({'id': self.vecs.iloc[top_sim_ix][return_data], 'score': np.round(
                sim[top_sim_ix], decimals=5), 'rank': rank})

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_words_by_id(self, doc_id, topn=10, return_data='id', return_similarity=False, duplicate_threshold=0.98, show_duplicates=False, serialize=False):
        self.check_wvecs()
        doc_vec = np.array(
            self.vecs[self.vecs['id'] == doc_id]['wvecs'].iloc[0]).reshape(1, -1)

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
        if 'wvecs' not in self.vecs.columns:
            raise ValueError('Document vectors not available!')

    def rescue_code(self, function):
        # http://blog.rtwilson.com/how-to-rescue-lost-code-from-a-jupyteripython-notebook/
        import inspect
        get_ipython().set_next_input(
            "".join(inspect.getsourcelines(function)[0]))

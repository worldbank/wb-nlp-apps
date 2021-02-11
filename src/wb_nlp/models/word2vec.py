'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import subprocess
import gc
import json
import os
from pathlib import Path
import pandas as pd
import gensim
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
from wb_nlp.interfaces import mongodb
from wb_nlp.utils.scripts import create_dask_cluster
from wb_nlp.types.models import Word2VecModelConfig, ModelRunInfo
from wb_nlp import dir_manager
from wb_nlp.processing.corpus import MultiDirGenerator
from wb_nlp.utils.scripts import (
    load_config, generate_model_hash,
    create_get_directory
)


class Word2VecModel:
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        raise_empty_doc_status=True
    ):
        cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", cleaning_config_id))

        assert cleaned_docs_dir.exists()

        cleaned_corpus_id = subprocess.check_output("md5sum " + cleaned_docs_dir.resolve().__str__(
        ) + "/*/*.txt | awk '{print $1}' | md5sum | awk '{print $1}'", shell=True)

        # The previous command returns a binary value like this: `b'07591edc636a73eafe9bea6eb2aaf3a6\n'` so we convert to str.
        cleaned_corpus_id = cleaned_corpus_id.strip().decode('utf-8')

        self.cleaning_config_id = cleaning_config_id
        self.cleaned_corpus_id = cleaned_corpus_id
        self.cleaned_docs_dir = cleaned_docs_dir

        model_configs_collection = mongodb.get_model_configs_collection()
        model_config = model_configs_collection.find_one(
            {"_id": model_config_id})

        # Do this to make sure that the config is consistent with the expected schema.
        Word2VecModelConfig(**model_config)

        model_name = model_config["meta"]["model_name"]

        assert model_name == "word2vec"
        assert gensim.__version__ == model_config['meta']['library_version']

        self.model_config_id = model_config_id
        self.model_config = model_config
        self.dim = self.model_config["word2vec_config"]["size"]

        model_run_info = dict(
            model_run_info_id="",
            model_name=model_name,
            model_config_id=self.model_config_id,
            processed_corpus_id=self.cleaned_corpus_id,
        )
        model_run_info_id = generate_model_hash(
            model_run_info)

        model_run_info = json.loads(ModelRunInfo(**model_run_info).json())

        assert model_run_info["model_run_info_id"] == model_run_info_id
        self.model_run_info = model_run_info

        self.model_id = model_run_info["model_run_info_id"]
        self.model = None
        self.raise_empty_doc_status = raise_empty_doc_status

        self.model_collection_id = f'{model_name}_{self.model_id}'

        model_dir = Path(dir_manager.get_path_from_root(
            "models", model_name, model_run_info_id))

        self.model_path = model_dir / f'{self.model_collection_id}.mm'

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
        del(self.model)

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
        if not self.model_path.parent.exists():
            self.model_path.parent.mkdir(parents=True)

        model_file_name = str(self.model_path)
        self.model.save(model_file_name)

        model_runs_info_collection = mongodb.get_model_runs_info_collection()
        model_run_info = dict(self.model_run_info)

        model_run_info['_id'] = self.model_run_info["model_run_info_id"]
        model_run_info['model_file_name'] = model_file_name[model_file_name.index(
            "/models/") + 1:]

        model_runs_info_collection.insert_one(model_run_info)

    def load_model(self):
        model_file_name = str(self.model_path)
        self.model = Word2Vec.load(model_file_name)

    def train_model(self, retrain=False, logger=None):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.

        if self.model_path.exists():
            print(
                'Warning: A model with the same configuration is available on disk. Loading...')
            self.load_model()
        elif self.model is None or retrain:
            file_generator = MultiDirGenerator(
                base_dir=self.cleaned_docs_dir,
                source_dir_name='',
                split=True,
                min_tokens=0,
                logger=logger
            )
            word2vec_params = self.model_config["word2vec_config"]
            word2vec_params.pop('word2vec_config_id')
            self.model = Word2Vec(
                sentences=file_generator,
                **word2vec_params
            )

            milvus_client = get_milvus_client()
            collection_name = self.model_collection_id

            if collection_name in milvus_client.list_collections():
                milvus_client.drop_collection(collection_name)

            self.save()

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

    import glob
    from pathlib import Path
    import hashlib
    import pandas as pd

    from wb_nlp.models import word2vec

    # doc_fnames = list(Path('./data/raw/sample_data/TXT_ORIG').glob('*.txt'))
    # doc_ids = [hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15]
    #            for p in doc_fnames]
    # corpus = ['WB'] * len(doc_ids)

    # doc_df = pd.DataFrame()
    # doc_df['id'] = doc_ids
    # doc_df['corpus'] = corpus
    # doc_df['text'] = [open(fn, 'rb').read().decode(
    #     'utf-8', errors='ignore') for fn in doc_fnames]

    wvec_model = word2vec.Word2VecModel(
        model_config_id="702984027cfedde344961b8b9461bfd3", cleaning_config_id="23f78350192d924e4a8f75278aca0e1c",
        raise_empty_doc_status=False)
    # %time
    wvec_model.train_model()

    wvec_model.build_doc_vecs(pool_workers=3)
    print(wvec_model.get_similar_words('bank'))
    print(wvec_model.get_similar_documents('bank'))
    print(wvec_model.get_similar_docs_by_id(doc_id='092d1961ab4f9a7'))
    print(wvec_model.get_similar_words_by_id(doc_id='092d1961ab4f9a7'))

    # print(wvec_model.get_similar_docs_by_id(doc_id='8314385c25c7c5e'))
    # print(wvec_model.get_similar_words_by_id(doc_id='8314385c25c7c5e'))

    milvus_client = get_milvus_client()
    collection_name = wvec_model.model_collection_id

    if collection_name in milvus_client.list_collections():
        milvus_client.drop_collection(collection_name)

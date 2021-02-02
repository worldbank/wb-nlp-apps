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


class LDAModel:
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        raise_empty_doc_status=True,
        log_level=logging.WARNING,
    ):
        configure_logger(log_level)
        self.logger = logging.getLogger(__file__)

        self.cleaning_config_id = cleaning_config_id
        self.model_config_id = model_config_id

        self.validate_and_prepare_requirements()

        self.model = None
        self.raise_empty_doc_status = raise_empty_doc_status

        # Try to load the model
        self.load()

        self.create_milvus_collection()

    def create_milvus_collection(self):
        self.milvus_vector_field_name = "embedding"

        self.collection_params = {
            "fields": [
                {"name": self.milvus_vector_field_name, "type": DataType.FLOAT_VECTOR,
                    "params": {"dim": self.dim}},
            ],
            "segment_row_limit": 4096,
            "auto_id": False
        }

        if self.model_collection_id not in get_milvus_client().list_collections():
            get_milvus_client().create_collection(
                self.model_collection_id, self.collection_params)

    def drop_milvus_collection(self):
        if self.model_collection_id in get_milvus_client().list_collections():
            get_milvus_client().drop_collection(self.model_collection_id)

    def validate_and_prepare_requirements(self):
        self.cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", self.cleaning_config_id))

        assert self.cleaned_docs_dir.exists()

        self.cleaned_corpus_id = get_cleaned_corpus_id(self.cleaned_docs_dir)

        model_configs_collection = mongodb.get_model_configs_collection()
        self.model_config = model_configs_collection.find_one(
            {"_id": self.model_config_id})

        # Do this to make sure that the config is consistent with the expected schema.
        LDAModelConfig(**self.model_config)

        self.model_name = self.model_config["meta"]["model_name"]

        assert self.model_name == "lda"
        assert gensim.__version__ == self.model_config['meta']['library_version']

        self.dim = self.model_config[f"{self.model_name}_config"]["num_topics"]

        self.dictionary_params = self.model_config['dictionary_config']
        processed_corpus_ids = [self.cleaned_corpus_id,
                                self.dictionary_params['dictionary_config_id']]
        self.processed_corpus_id = "_".join(processed_corpus_ids)

        self.dictionary_file = self.cleaned_docs_dir / \
            f"dictionary-{self.processed_corpus_id}.gensim.dict"
        self.corpus_path = self.cleaned_docs_dir / \
            f"bow_corpus-{self.processed_corpus_id}.mm"

        self.model_run_info = dict(
            model_run_info_id="",
            model_name=self.model_name,
            model_config_id=self.model_config_id,
            processed_corpus_id=self.processed_corpus_id,
        )
        self.model_id = generate_model_hash(
            self.model_run_info)

        self.model_run_info = json.loads(
            ModelRunInfo(**self.model_run_info).json())

        assert self.model_run_info["model_run_info_id"] == self.model_id

        self.model_collection_id = f'{self.model_name}_{self.model_id}'

        self.model_dir = Path(dir_manager.get_path_from_root(
            "models", self.model_name, self.model_id))

        self.model_file_name = self.model_dir / \
            f'{self.model_collection_id}.bz2'

    def get_training_data(self):
        """
        This method returns a transformed corpus that can be used to train the model.
        This is specifically designed to dump the transformed corpus to disk and load it if available.
        There is an implicit assumption that the compute resources is large enough to handle the data.
        """
        checkpoint_log(
            self.logger, timer=None, message='Loading or generating dictionary...')

        if self.corpus_path.exists():
            self.logger.info('Loading saved corpus and dictionary...')
            assert self.dictionary_file.exists()

            g_dict = Dictionary.load(str(self.dictionary_file))
            corpus = MmCorpus(str(self.corpus_path))

        else:
            file_generator = MultiDirGenerator(
                base_dir=self.cleaned_docs_dir,
                source_dir_name='',
                split=True,
                min_tokens=self.model_config['min_tokens'],
                logger=self.logger
            )

            if self.dictionary_file.exists():
                g_dict = Dictionary.load(str(self.dictionary_file))
            else:
                self.logger.info('Training dictionary...')
                g_dict = Dictionary(file_generator)

                g_dict.filter_extremes(
                    no_below=self.dictionary_params['no_below'],
                    no_above=self.dictionary_params['no_above'],
                    keep_n=self.dictionary_params['keep_n'],
                    keep_tokens=self.dictionary_params['keep_tokens'])

                g_dict.id2token = {id: token for token,
                                   id in g_dict.token2id.items()}

                g_dict.save(str(self.dictionary_file))

            self.logger.info('Generating corpus...')
            corpus = [g_dict.doc2bow(d) for d in file_generator]

            self.logger.info('Saving corpus to %s...', self.corpus_path)
            MmCorpus.serialize(str(self.corpus_path), corpus)

        checkpoint_log(
            self.logger, timer=None, message='Loading or generating corpus...')

        return dict(
            corpus=corpus,
            g_dict=g_dict,
        )

    def clear(self):
        del(self.model)

        self.model = None

        gc.collect()

    def save(self):
        self.save_model()

    def load(self):
        self.load_model()

        if self.model:
            # Make sure that the dimensionality uses the one in the trained model.
            if self.dim != self.model.num_topics:
                print(
                    'Warning: dimension declared is not aligned with loaded model. Using loaded model dim.')
                self.dim = self.model.num_topics

    def save_model(self):
        self.check_model()
        if not self.model_file_name.parent.exists():
            self.model_file_name.parent.mkdir(parents=True)

        model_file_name = str(self.model_file_name)
        self.model.save(model_file_name)

        model_runs_info_collection = mongodb.get_model_runs_info_collection()
        model_run_info = dict(self.model_run_info)

        model_run_info['_id'] = self.model_run_info["model_run_info_id"]
        model_run_info['model_file_name'] = model_file_name[model_file_name.index(
            "/models/") + 1:]

        model_runs_info_collection.insert_one(model_run_info)
        self.logger.info(self.model.print_topics())

    def load_model(self):
        model_file_name = str(self.model_file_name)
        try:
            self.model = LdaMulticore.load(model_file_name)
        except FileNotFoundError:
            self.model = None

    def train_model(self, retrain=False):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.
        if self.model_file_name.exists():
            print(
                'Warning: A model with the same configuration is available on disk. Loading...')
            self.load_model()
        elif self.model is None or retrain:
            corpus_data = self.get_training_data()

            lda_params = dict(self.model_config[f"{self.model_name}_config"])
            lda_params['id2word'] = dict(corpus_data["g_dict"].id2token)
            lda_params.pop(f'{self.model_name}_config_id')

            self.model = LdaMulticore(corpus_data["corpus"], **lda_params)

            self.drop_milvus_collection()

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

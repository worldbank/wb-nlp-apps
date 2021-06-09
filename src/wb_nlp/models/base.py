'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
from functools import partial, lru_cache
import os
import gc
import json
import logging
from pathlib import Path
import pickle
import gensim
from gensim.corpora import Dictionary, MmCorpus
from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
import pandas as pd
import numpy as np
from contexttimer import Timer
import joblib
from joblib import delayed, Parallel

from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

from milvus import DataType

from wb_cleaning.cleaning import stopwords
from wb_cleaning.processing.corpus import MultiDirGenerator, replace_phrases

from wb_nlp.interfaces.milvus import (
    get_milvus_client,
    get_collection_ids,
    get_embedding_dsl,
    get_hex_id,
    get_int_id,
)
from wb_nlp.interfaces import mongodb, elasticsearch
from wb_nlp.types.models import ModelRunInfo, ModelTypes
from wb_nlp import dir_manager
from wb_nlp.utils.scripts import (
    configure_logger,
    create_dask_cluster,
    generate_model_hash,
    checkpoint_log,
    get_cleaned_corpus_id,
    get_cleaner,
)
from wb_nlp import live_cache


def read_text_file(fname):
    with open(fname, "rb") as open_file:
        text = open_file.read().decode("utf-8", errors="ignore")

    return text


class BaseModel:
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class,
        model_config_type,
        expected_model_name,
        model_run_info_description="",
        model_run_info_id=None,
        raise_empty_doc_status=True,
        log_level=logging.INFO,
    ):
        configure_logger(log_level)
        self.log_level = log_level
        self.logger = logging.getLogger(__file__)
        self.trainable = False

        self.model_class = model_class  # Example: LdaMulticore
        self.model_config_type = model_config_type  # Example: LDAModelConfig
        self.expected_model_name = expected_model_name

        if model_run_info_id is None:
            self.cleaning_config_id = cleaning_config_id
            self.model_config_id = model_config_id
            self.model_run_info_description = model_run_info_description

            self.validate_and_prepare_requirements()
            self.trainable = True

        else:
            self.validate_and_load_model_run_info_from_db(
                model_run_info_id=model_run_info_id,
                model_config_id=model_config_id,
                cleaning_config_id=cleaning_config_id,
            )
            self.trainable = False

        self.model = None
        self.mallet_model = None
        self.raise_empty_doc_status = raise_empty_doc_status

        # # Try to load the model
        self.logger.info("Start loading model...")
        self.load()
        self.set_model_specific_attributes()

        self.logger.info("Creating milvus collection...")
        self.create_milvus_collection()

        self.doc_topic_meta_fields = [
            "adm_region", "country", "corpus", "date_published",
            "doc_type", "geo_region", "major_doc_type", "topics_src", "year"]

    def log(self, message):

        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def set_model_specific_attributes(self):
        pass

    def clean_text(self, document, as_string=True):
        cleaner = get_cleaner(self.cleaning_config_id)
        tokens = cleaner.get_clean_tokens(document)

        if as_string:
            tokens = " ".join(tokens)
        return tokens

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

    def get_doc_id_from_int_id(self, int_id):
        return live_cache.DOCS_INT_ID_TO_ID[int_id]
        # # docs_metadata_collection = mongodb.get_docs_metadata_collection()
        # docs_metadata_collection = mongodb.get_collection(
        #     db_name="test_nlp", collection_name="docs_metadata")

        # res = docs_metadata_collection.find_one(
        #     {"int_id": int_id}, projection=["id"])
        # return res["id"]

    def get_int_id_from_doc_id(self, doc_id):
        # docs_metadata_collection = mongodb.get_docs_metadata_collection()
        docs_metadata_collection = mongodb.get_collection(
            db_name="test_nlp", collection_name="docs_metadata")

        res = docs_metadata_collection.find_one(
            {"id": doc_id}, projection=["int_id"])
        return res["int_id"]

    def set_processed_corpus_id(self):
        # Generate an identifier corresponding to the processed data.
        # If no additional processing is needed such as in word2vec,
        # this is set to the cleaned_corpus_id, otherwise we compute
        # additional identifiers.
        if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:
            self.dictionary_params = self.model_config['dictionary_config']
            processed_corpus_ids = [self.cleaned_corpus_id,
                                    self.dictionary_params['dictionary_config_id']]
            self.processed_corpus_id = "_".join(processed_corpus_ids)

            self.dictionary_file = self.cleaned_docs_dir / \
                f"dictionary-{self.processed_corpus_id}.gensim.dict"
            self.corpus_path = self.cleaned_docs_dir / \
                f"bow_corpus-{self.processed_corpus_id}.mm"
            self.corpus_ids_path = self.cleaned_docs_dir / \
                f"bow_corpus_ids-{self.processed_corpus_id}.list.pickle"
            self.corpus_token_counts_path = self.cleaned_docs_dir / \
                f"bow_corpus_token_counts-{self.processed_corpus_id}.dict.pickle"

        elif self.model_name == ModelTypes.word2vec.value:
            self.processed_corpus_id = self.cleaned_corpus_id
        else:
            raise ValueError(f"Unknown model name: {self.model_name}...")

    def validate_and_prepare_requirements(self):
        self.cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", self.cleaning_config_id))

        # Make sure that the directory where we expect the cleaned files are exists.
        assert self.cleaned_docs_dir.exists()

        # We get the unique identifier for the corpus. This is based on the
        # hash of the hashes of the individual files.
        self.cleaned_corpus_id = get_cleaned_corpus_id(self.cleaned_docs_dir)

        self.validate_and_load_model_config()

        self.set_processed_corpus_id()

        self.set_and_validate_model_run_info()

        self.set_trained_model_attributes()

    def set_and_validate_model_run_info(self):
        # Define the metadata corresponding to the model.
        # The model_run_info specifies the set of metadata
        # necessary to replicate the model from scratch.
        self.model_run_info = dict(
            model_run_info_id="",
            model_name=self.model_name,
            model_config_id=self.model_config_id,
            cleaning_config_id=self.cleaning_config_id,
            processed_corpus_id=self.processed_corpus_id,
        )
        self.model_id = generate_model_hash(
            self.model_run_info)

        self.model_run_info = json.loads(
            ModelRunInfo(**self.model_run_info).json())

        self.model_run_info["description"] = self.model_run_info_description

        assert self.model_run_info["model_run_info_id"] == self.model_id

    def validate_and_load_model_run_info_from_db(self, model_run_info_id, model_config_id, cleaning_config_id):
        # Load model_run_info from db.
        model_runs_info_collection = mongodb.get_model_runs_info_collection()
        model_run_info = model_runs_info_collection.find_one(
            {"model_run_info_id": model_run_info_id})

        assert model_config_id == model_run_info["model_config_id"]
        assert cleaning_config_id == model_run_info["cleaning_config_id"]

        self.model_run_info = model_run_info
        self.model_name = model_run_info["model_name"]
        self.model_config_id = model_run_info["model_config_id"]
        self.cleaning_config_id = model_run_info["cleaning_config_id"]
        self.processed_corpus_id = model_run_info["processed_corpus_id"]
        self.model_id = model_run_info["model_run_info_id"]
        self.model_run_info_description = model_run_info["description"]

        self.cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", self.cleaning_config_id))

        # Make sure that the directory where we expect the cleaned files are exists.
        assert self.cleaned_docs_dir.exists()

        self.validate_and_load_model_config()

        self.set_trained_model_attributes()

    def validate_and_load_model_config(self):
        # Get the configuration of the model from mongodb.
        model_configs_collection = mongodb.get_model_configs_collection()
        self.model_config = model_configs_collection.find_one(
            {"_id": self.model_config_id})

        # Do this to make sure that the config is consistent with the expected schema.
        self.model_config_type(**self.model_config)
        self.model_name = self.model_config["meta"]["model_name"]

        # Perform basic validation of the configuration.
        assert self.model_name == self.expected_model_name
        assert gensim.__version__ == self.model_config['meta']['library_version']

        # Set the `dim` attribute to be used when creating the milvus
        # index for the model.
        params = self.model_config[f"{self.model_name}_config"]
        self.dim = params.get("num_topics", params.get("size"))

    def set_trained_model_attributes(self):
        # Set attributes corresponding where we want the trained model
        # will be saved.
        self.model_collection_id = f'{self.model_name}_{self.model_id}'

        self.model_dir = Path(dir_manager.get_path_from_root(
            "models", self.model_name, self.model_id))

        self.model_file_name = self.model_dir / \
            f'{self.model_collection_id}.bz2'

    def get_training_corpus(self):
        """
        This method returns a transformed corpus that can be used to train the model.
        This is specifically designed to dump the transformed corpus to disk and load it if available.
        There is an implicit assumption that the compute resources is large enough to handle the data.
        """
        if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:
            checkpoint_log(
                self.logger, timer=None, message='Loading or generating dictionary...')

            if self.corpus_path.exists():
                self.logger.info('Loading saved corpus and dictionary...')
                self.logger.info("Corpus path %s", self.corpus_path)
                assert self.dictionary_file.exists()

                g_dict = Dictionary.load(str(self.dictionary_file))
                corpus = MmCorpus(str(self.corpus_path))

                with open(self.corpus_ids_path, 'rb') as open_file:
                    corpus_ids = pickle.load(open_file)

                with open(self.corpus_token_counts_path, 'rb') as open_file:
                    corpus_token_counts = pickle.load(open_file)

            else:
                file_generator = MultiDirGenerator(
                    base_dir=self.cleaned_docs_dir,
                    source_dir_name='',
                    split=True,
                    min_tokens=self.model_config['min_tokens'],
                    include_extra=False,
                    cached=True,
                    logger=self.logger
                )

                if self.dictionary_file.exists():
                    g_dict = Dictionary.load(str(self.dictionary_file))
                else:
                    self.logger.info('Training dictionary...')
                    g_dict = Dictionary(
                        content_doc_id[0] for content_doc_id in file_generator)

                    g_dict.filter_extremes(
                        no_below=self.dictionary_params['no_below'],
                        no_above=self.dictionary_params['no_above'],
                        keep_n=self.dictionary_params['keep_n'],
                        keep_tokens=self.dictionary_params['keep_tokens'])

                    g_dict.id2token = {id: token for token,
                                       id in g_dict.token2id.items()}

                    g_dict.save(str(self.dictionary_file))

                self.logger.info('Generating corpus...')
                corpus = []
                corpus_ids = []
                corpus_token_counts = {}

                for doc_content, doc_id in file_generator:
                    corpus.append(g_dict.doc2bow(doc_content))
                    corpus_ids.append(doc_id)
                    corpus_token_counts[doc_id] = len(doc_content)

                # Free up memory by clearing the document cache
                file_generator.clear_cache()

                self.logger.info('Saving corpus to %s...', self.corpus_path)
                MmCorpus.serialize(str(self.corpus_path), corpus)

                self.logger.info('Saving corpus ids to %s...',
                                 self.corpus_ids_path)
                with open(self.corpus_ids_path, 'wb') as open_file:
                    pickle.dump(corpus_ids, open_file)
                with open(self.corpus_token_counts_path, 'wb') as open_file:
                    pickle.dump(corpus_token_counts, open_file)

            checkpoint_log(
                self.logger, timer=None, message='Loading or generating corpus...')

            self.g_dict = g_dict
            self.corpus_ids = corpus_ids
            self.corpus_token_counts = corpus_token_counts

        elif self.model_name == ModelTypes.word2vec.value:
            corpus = MultiDirGenerator(
                base_dir=self.cleaned_docs_dir,
                source_dir_name='',
                split=True,
                min_tokens=0,
                include_extra=True,
                return_doc_id=False,
                cached=True,
                logger=self.logger
            )

        return corpus

    def clear(self):
        del(self.model)

        self.model = None

        gc.collect()

    def save(self):
        self.save_model()

    def load(self):
        self.load_model()

        if self.model:
            if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:
                dim = self.model.num_topics
            elif self.model_name == ModelTypes.word2vec.value:
                dim = self.model.wv.vector_size

            # Make sure that the dimensionality uses the one in the trained model.
            if self.dim != dim:
                self.log(
                    'Warning: dimension declared is not aligned with loaded model. Using loaded model dim.')
                self.dim = dim

            self.set_model_word_vectors()

    def save_model(self):
        if not self.trainable:
            self.log("Model state is set to trainable=False and can't be saved!")
            return

        self.check_model()
        model_runs_info_collection = mongodb.get_model_runs_info_collection()
        # model_runs_info_collection.delete_many({})
        model_runs_info_collection.delete_many(
            {"_id": self.model_run_info["model_run_info_id"]})

        if not self.model_file_name.exists():
            model_runs_info_collection.delete_many(
                {"_id": self.model_run_info["model_run_info_id"]})

            if not self.model_file_name.parent.exists():
                self.model_file_name.parent.mkdir(parents=True)

        model_file_name = str(self.model_file_name)

        if self.model_name == ModelTypes.mallet.value:
            self.mallet_model.save(model_file_name)
        else:
            self.model.save(model_file_name)

        model_run_info = dict(self.model_run_info)

        model_run_info['_id'] = self.model_run_info["model_run_info_id"]
        model_run_info['model_file_name'] = model_file_name[model_file_name.index(
            "/models/") + 1:]

        model_runs_info_collection.insert_one(model_run_info)

        if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:
            self.logger.info(self.model.print_topics())

        self.set_model_word_vectors()

    def load_model(self):
        self.logger.info(f"Model path: {self.model_file_name}")

        if not self.model_file_name.exists():
            self.model = None
            return

        model_file_name = str(self.model_file_name)

        try:
            self.logger.info("Actually loading model...")
            self.model = self.model_class.load(model_file_name)
            self.logger.info("Model loaded...")

            # model_runs_info_collection = mongodb.get_model_runs_info_collection()
            # assert model_runs_info_collection.find_one({"_id": self.model_run_info["model_run_info_id"]}), "Trained model present but `model_run_info` not in db, aborting load... Options: You can delete the model and retrain. Alternatively, if `model_run_info` is stored available, please make sure to upload it in the correct collection. Also note that the Milvus table must exist!"

            if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:

                self.g_dict = Dictionary()
                self.g_dict.id2token = self.model.id2word
                self.g_dict.token2id = {k: v for v,
                                        k in self.g_dict.id2token.items()}

                if self.model_name == ModelTypes.mallet.value:
                    self.mallet_model = self.model

                    self.model = malletmodel2ldamodel(
                        self.model, iterations=self.model.iterations)

            # Force save model to also update the `model_run_info` on db.
            self.save_model()
            # self.set_model_word_vectors()

        except FileNotFoundError:
            self.model = None

    def set_model_word_vectors(self):
        if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:

            self.word_vectors = self.model.expElogbeta
            self.word_vectors = self.word_vectors / \
                (1e-10 + self.word_vectors.sum(axis=0))

            self.word_vectors = self.word_vectors.T
            self.index2word = self.model.id2word

        elif self.model_name == ModelTypes.word2vec.value:
            self.word_vectors = self.model.wv.vectors
            self.index2word = self.model.wv.index2word

    def get_model_params(self):
        params = dict(self.model_config[f"{self.model_name}_config"])
        params.pop(f'{self.model_name}_config_id')

        if self.model_name in [ModelTypes.lda.value, ModelTypes.mallet.value]:
            params['id2word'] = dict(self.g_dict.id2token)

        cpu_count = os.cpu_count()
        if self.model_name == ModelTypes.lda.value:
            # Note however that for hyper-threaded CPUs,
            # this estimation returns a too high number – set workers
            # directly to the number of your real cores (not hyperthreads)
            # minus one, for optimal performance.
            params["workers"] = (cpu_count // 2) - 1
        else:
            if cpu_count >= 8:
                cpu_count = cpu_count - 4
            else:
                cpu_count = max(1, cpu_count - 1)

            params["workers"] = cpu_count

        return params

    def train_model(self, retrain=False):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.
        if not self.trainable:
            self.log(
                "Model is set to trainable=False state since it was loaded from an existing model_run_info_id. Training will not continue!")
            return

        if self.model_file_name.exists() and not retrain:
            self.log(
                'Warning: A model with the same configuration is available on disk. Loading...')
            self.load_model()
        elif self.model is None or retrain:
            self.log(
                'Starting model training...')
            corpus = self.get_training_corpus()
            params = self.get_model_params()

            self.model = self.model_class(corpus, **params)

            self.drop_milvus_collection()

            self.save()

        else:
            self.log('Warning: Model already trained. Not doing anything...')

    def check_model(self):
        if self.model is None:
            raise ValueError('Model not trained!')

    def check_wvecs(self):
        collection_doc_ids = get_collection_ids(self.model_collection_id)

        if len(collection_doc_ids) == 0:
            raise ValueError('Document vectors not available!')

    def transform_doc(self, document, normalize=True, tolist=False):
        # This function is the primary method of converting a document
        # into its vector representation based on the model.
        # This should be implemented in the respective models.
        # The expected output is a dictionary with keys:
        # - doc_vec  # numpy array of shape (1, self.dim)
        # - success  # Whether the transformation went successfully
        self.check_model()
        return dict(doc_vec=None, success=None)

    def transform_docs(self, docs, normalize=True, tolist=False):
        """
        This method accepts a dataframe as input that must contain a `phrase_text` column.
        It will expand the dataframe to include derived columns, namely, `doc_vec` and `success`.
        """
        p_transform_doc = partial(
            self.transform_doc, normalize=normalize, tolist=tolist)
        cols = ["doc_vec", "success"]

        docs[cols] = docs["phrase_text"].map(
            p_transform_doc).apply(pd.Series)[cols]

        return docs

    def process_doc(self, doc, normalize=True):
        """
        This method converts the text described by the `doc` object into its vector representation.
        This function must only be used a cleaned text. No additional processing will be done excep lower casing.
        This method accepts a `doc` object containing the following fields from the docs_metadata:
        - id
        - int_id
        - hex_id
        - corpus

        A `text` field could be inserted if available. Otherwise, the text will be loaded from disk.
        """
        text = doc.get('text')

        if not text:
            fname = self.cleaned_docs_dir / doc["corpus"] / f"{doc['id']}.txt"
            with open(fname, "rb") as open_file:
                text = open_file.read().decode("utf-8", errors="ignore")

        text = replace_phrases(text)

        return self.transform_doc(text.lower(), normalize=normalize)

    def process_docs(self, docs, normalize=True):
        docs["phrase_text"] = docs["text"].map(replace_phrases)
        return self.transform_docs(docs, normalize=normalize)

    def normalize_vectors(self, vectors):
        return [doc_vec / np.linalg.norm(doc_vec, ord=2) for doc_vec in vectors]

    def build_docs_group(self, docs, is_topic_model, group_id, max_group, collection_name, partition_group):
        milvus_client = get_milvus_client()
        normalize = not is_topic_model

        print(f"Loading group {group_id + 1} / {max_group + 1}...")
        docs["text"] = docs.apply(
            lambda _doc: read_text_file(self.cleaned_docs_dir / _doc["corpus"] / f"{_doc['id']}.txt"), axis=1)

        docs["_l"] = docs["text"].map(len)
        docs = docs.sort_values("_l")

        self.log(docs.head(20).set_index("id")["text"].map(
            lambda x: x[:100]))

        self.log(
            f"Smallest and largest files for this group has {docs.iloc[0]['_l']} and {docs.iloc[-1]['_l']} characters, respectively...")

        self.log(
            f"Finished reading {len(docs)} files, starting vector generation...")

        results = self.process_docs(docs, normalize=normalize)

        print(f"{group_id + 1}. Finished vector generation, storing vectors to db...")

        results = [(ix, p['doc_vec'].flatten())
                   for ix, (_, p) in enumerate(results.iterrows()) if p['success']]

        if len(results) == 0:
            return False

        locs, vectors = list(zip(*results))
        doc_int_ids = docs.iloc[list(
            locs)]['int_id'].tolist()
        doc_ids = docs.iloc[list(
            locs)]['id'].tolist()

        # If LDA model, dump topics in mongodb document_topics collection.
        if is_topic_model:

            print("FILLING TOPIC DB")
            # mongodb.get_document_topics_collection().delete_many(
            #     {"id": {"$in": doc_ids}, "model_run_info_id": self.model_run_info["model_run_info_id"]})

            # mongodb.get_document_topics_collection().insert_many(
            #     [dict(
            #         model_run_info_id=self.model_run_info["model_run_info_id"],
            #         id=doc_id,
            #         _id=f"{self.model_run_info['model_run_info_id']}-{doc_id}",
            #         topics={
            #             f"topic_{topic_id}": value for topic_id, value in enumerate(topic_list)}
            #     ) for doc_id, topic_list in zip(doc_ids, vectors)]
            # )

            elasticsearch.store_docs_topics(
                doc_ids=doc_ids,
                vectors=vectors,
                model_run_info_id=self.model_run_info['model_run_info_id'],
                metadata=docs[self.doc_topic_meta_fields +
                              ["id"]].set_index("id").T.to_dict(),
                ignore_existing=False)

            # for doc_id, topic_list in zip(doc_ids, vectors):
            #     topics = {f"topic_{topic_id}": value for topic_id, value in enumerate(topic_list)}

            #     elasticsearch.store_doc_topics(
            #         doc_id=doc_id,
            #         topics=topics,
            #         model_run_info_id=self.model_run_info['model_run_info_id'])

        entities = [
            {"name": self.milvus_vector_field_name, "values": self.normalize_vectors(vectors) if is_topic_model else vectors,
                "type": DataType.FLOAT_VECTOR},
        ]

        if not milvus_client.has_partition(collection_name, partition_group):
            milvus_client.create_partition(
                collection_name, partition_group)

        ids = milvus_client.insert(collection_name, entities,
                                   doc_int_ids, partition_tag=partition_group)

        assert len(set(ids).difference(
            doc_int_ids)) == 0

        milvus_client.flush([collection_name])

        return True

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

        collection_doc_ids = list(set(get_collection_ids(collection_name)))

        projection = ["id", "int_id", "hex_id", "corpus"]
        projection = [
            i for i in projection if i not in self.doc_topic_meta_fields] + self.doc_topic_meta_fields

        cleaned_ids = [i.stem for i in self.cleaned_docs_dir.glob("*/*.txt")]

        docs_metadata_df = pd.DataFrame(
            list(docs_metadata_collection.find(projection=projection)), columns=projection)

        docs_for_processing = docs_metadata_df[
            (~docs_metadata_df['int_id'].isin(collection_doc_ids)) & docs_metadata_df["id"].isin(cleaned_ids)]

        print(
            f"Collection size: {len(collection_doc_ids)}\nCleaned ids count: {len(cleaned_ids)}\ndocs_metadata_df size: {docs_metadata_df.shape[0]}")
        print(
            f"Sample milvus_ids: {collection_doc_ids[:10]}\nSample clean_ids: {cleaned_ids[:10]}")

        dask_client = create_dask_cluster(
            logger=self.logger, n_workers=pool_workers)

        is_topic_model = self.model_name in [
            ModelTypes.lda.value, ModelTypes.mallet.value]

        print(f"IS TOPIC MODEL: {is_topic_model}")

        print(f"Processing {docs_for_processing.shape[0]} files...")

        try:
            with joblib.parallel_backend('dask'):
                if not docs_for_processing.empty:
                    # Perform normalization of topic model vectors only when we load them in Milvus.
                    normalize = not is_topic_model
                    for partition_group, sub_docs in docs_for_processing.groupby('corpus'):
                        # Partition corpus into sub groups of size at most 1000
                        group_size = 1000
                        if group_size < len(sub_docs):
                            group_value = np.array(
                                range(len(sub_docs))) % (len(sub_docs) // group_size)
                        else:
                            group_value = np.zeros(len(sub_docs))

                        max_group = max(group_value)

                        print(f"Starting parallel process...")

                        results = Parallel(verbose=10, batch_size='auto')(
                            delayed(self.build_docs_group)(docs, is_topic_model, group_id, max_group, collection_name, partition_group) for group_id, docs in sub_docs.groupby(group_value))

                        # for group_id, sub_sub_docs in sub_docs.groupby(group_value):
                        #     self.log(
                        #         f"Loading group {group_id + 1} / {max_group + 1}...")
                        #     sub_sub_docs["text"] = sub_sub_docs.apply(
                        #         lambda _doc: read_text_file(self.cleaned_docs_dir / _doc["corpus"] / f"{_doc['id']}.txt"), axis=1)

                        #     sub_sub_docs["_l"] = sub_sub_docs["text"].map(len)
                        #     sub_sub_docs = sub_sub_docs.sort_values("_l")

                        #     self.log(sub_sub_docs.head(20).set_index("id")["text"].map(
                        #         lambda x: x[:100]))

                        #     self.log(
                        #         f"Smallest and largest files for this group has {sub_sub_docs.iloc[0]['_l']} and {sub_sub_docs.iloc[-1]['_l']} characters, respectively...")

                        #     self.log(
                        #         f"Finished reading {len(sub_sub_docs)} files, starting vector generation...")

                        #     self.build_docs_group(
                        #         sub_sub_docs, is_topic_model, milvus_client, collection_name, partition_group)

                        # results = Parallel(verbose=10, batch_size='auto')(
                        #     delayed(self.process_doc)(doc, normalize) for idx, doc in sub_sub_docs.iterrows())

                        # self.log(
                        #     f"Finished vector generation, storing vectors to db...")

                        # results = [(ix, p['doc_vec'].flatten())
                        #            for ix, p in enumerate(results) if p['success']]

                        # if len(results) == 0:
                        #     continue

                        # locs, vectors = list(zip(*results))
                        # sub_sub_int_ids = sub_sub_docs.iloc[list(
                        #     locs)]['int_id'].tolist()
                        # sub_sub_ids = sub_sub_docs.iloc[list(
                        #     locs)]['id'].tolist()

                        # # If LDA model, dump topics in mongodb document_topics collection.
                        # if is_topic_model:
                        #     print("FILLING TOPIC DB")
                        #     mongodb.get_document_topics_collection().delete_many(
                        #         {"id": {"$in": sub_sub_ids}})

                        #     mongodb.get_document_topics_collection().insert_many(
                        #         [dict(
                        #             model_run_info_id=self.model_run_info["model_run_info_id"],
                        #             id=doc_id,
                        #             _id=doc_id,
                        #             topics={
                        #                 f"topic_{topic_id}": value for topic_id, value in enumerate(topic_list)}
                        #         ) for doc_id, topic_list in zip(sub_sub_ids, vectors)]
                        #     )

                        # entities = [
                        #     {"name": self.milvus_vector_field_name, "values": self.normalize_vectors(vectors) if is_topic_model else vectors,
                        #         "type": DataType.FLOAT_VECTOR},
                        # ]

                        # if not milvus_client.has_partition(collection_name, partition_group):
                        #     milvus_client.create_partition(
                        #         collection_name, partition_group)

                        # ids = milvus_client.insert(collection_name, entities,
                        #                            sub_sub_int_ids, partition_tag=partition_group)

                        # assert len(set(ids).difference(
                        #     sub_sub_int_ids)) == 0

                        # milvus_client.flush([collection_name])
        except Exception as e:
            dask_client.close()
            raise(e)
        finally:
            dask_client.close()

    @lru_cache(maxsize=128)
    def get_doc_vec(self, document, normalize=True, assert_success=True, flatten=True):
        document = replace_phrases(document)
        doc_vec_payload = self.transform_doc(document, normalize=normalize)
        doc_vec = doc_vec_payload['doc_vec']

        if assert_success and not doc_vec_payload['success']:
            raise ValueError("Document was mapped to the zero vector!")

        return doc_vec.flatten() if flatten else doc_vec

    @lru_cache(maxsize=128)
    def cached_milvus_result(self, document, topk, metric_type="IP"):
        # print(f"First access for {document}...")
        with Timer() as timer:
            print(f"CMR Elapsed 1: {timer.elapsed}")
            doc_vec = self.get_doc_vec(
                document, normalize=True, assert_success=True, flatten=True)

            # topk = 1000  # from_result + (2 * size)  # Add buffer
            # topk = (((from_result + size) // batch_size) + 1) * batch_size
            # print(f"CMR Elapsed 2: {timer.elapsed}")
            # dsl = get_embedding_dsl(
            #     doc_vec, topk, vector_field_name=self.milvus_vector_field_name, metric_type=metric_type)
            # print(f"CMR Elapsed 3: {timer.elapsed}")
            # results = get_milvus_client().search(self.model_collection_id, dsl)
            results = self.search_milvus(
                doc_vec, topk, vector_field_name=self.milvus_vector_field_name, metric_type="IP")

            print(f"CMR Elapsed 4: {timer.elapsed}")
            entities = []
            for position, ent in enumerate(results[0]):
                entities.append(
                    dict(
                        id=ent.id,
                        distance=ent.distance,
                        position=position)
                )
            print(entities[:10])

            print(f"CMR Elapsed 4: {timer.elapsed}")

            return entities

    def search_milvus(self, doc_vec, topk, vector_field_name, metric_type="IP"):

        # topk = 1000  # from_result + (2 * size)  # Add buffer
        # topk = (((from_result + size) // batch_size) + 1) * batch_size
        # print(f"CMR Elapsed 2: {timer.elapsed}")
        dsl = get_embedding_dsl(
            doc_vec, topk, vector_field_name=vector_field_name, metric_type=metric_type)
        # print(f"CMR Elapsed 3: {timer.elapsed}")
        return get_milvus_client().search(self.model_collection_id, dsl)

    def search_similar_documents(self, document, duplicate_threshold=0.999, show_duplicates=False, serialize=False, metric_type="IP", from_result=0, size=10, batch_size=100):
        # document: any text
        # topn: number of returned related documents in the database
        # return_data: string corresponding to a column in the docs or list of column names
        # duplicate_threhold: threshold that defines a duplicate document based on similarity score
        # show_duplicates: option if exact duplicates of documents are to be considered as return documents
        self.check_wvecs()

        # doc_vec = self.get_doc_vec(
        #     document, normalize=True, assert_success=True, flatten=True)

        # topk = from_result + (2 * size)  # Add buffer
        # dsl = get_embedding_dsl(
        #     doc_vec, topk, vector_field_name=self.milvus_vector_field_name, metric_type=metric_type)
        # results = get_milvus_client().search(self.model_collection_id, dsl)

        # entities = results[0]

        with Timer() as timer:
            print(f"SSD Elapsed 1: {timer.elapsed}")
            topk = (((from_result + size) // batch_size) + 1) * batch_size
            entities = self.cached_milvus_result(
                document, topk=topk, metric_type=metric_type)

            print(f"SSD Elapsed 2: {timer.elapsed}")
            payload = []
            for ent in entities:

                if from_result > ent["position"]:
                    continue

                if not show_duplicates:
                    # TODO: Make sure that this is true for Milvus.
                    # If we change the metric_type, this should be adjusted somehow.
                    if ent["distance"] > duplicate_threshold:
                        continue

                payload.append({'id': self.get_doc_id_from_int_id(ent["id"]), 'score': float(np.round(
                    ent["distance"], decimals=5)), 'rank': ent["position"] + 1})

                if len(payload) == size:
                    break

            print(f"SSD Elapsed 3: {timer.elapsed}")
            payload = sorted(payload, key=lambda x: x['rank'])
            if serialize:
                payload = pd.DataFrame(payload).to_json()

            print(f"SSD Elapsed 4: {timer.elapsed}")

            return payload

    def get_similar_documents(self, document, topn=10, duplicate_threshold=0.999, show_duplicates=False, serialize=False, metric_type="IP"):
        # document: any text
        # topn: number of returned related documents in the database
        # return_data: string corresponding to a column in the docs or list of column names
        # duplicate_threhold: threshold that defines a duplicate document based on similarity score
        # show_duplicates: option if exact duplicates of documents are to be considered as return documents
        return self.search_similar_documents(
            document=document,
            duplicate_threshold=duplicate_threshold,
            show_duplicates=show_duplicates,
            serialize=serialize,
            metric_type=metric_type,
            from_result=0,
            size=topn,
        )

    def get_similar_words(self, document, topn=10, serialize=False, metric="cosine_similarity"):

        buffer_topn = 2 * topn
        doc_vec = self.get_doc_vec(
            document, normalize=True, assert_success=True, flatten=False)

        # self.log(
        #     f"doc_vec shape: {doc_vec.shape}, word_vectors shape: {self.word_vectors.shape}")

        if cosine_similarity.__name__ == metric:
            sim = cosine_similarity(doc_vec, self.word_vectors).flatten()
            argidx = sim.argsort()[-buffer_topn:][::-1]
        elif euclidean_distances.__name__ == metric:
            sim = euclidean_distances(doc_vec, self.word_vectors).flatten()
            argidx = sim.argsort()[:buffer_topn]
        else:
            raise ValueError(f"Unknow metric: `{metric}")

        payload = []
        rank = 1
        for ix, top_sim_ix in enumerate(argidx, 1):
            word = self.index2word[top_sim_ix]
            if word in stopwords.noise_words:
                continue

            payload.append({"id": int(top_sim_ix), 'word': word, 'score': float(np.round(
                sim[top_sim_ix], decimals=5)), 'rank': rank})

            rank += 1
            if rank > topn:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_milvus_doc_vector_by_doc_id(self, doc_id):
        int_id = self.get_int_id_from_doc_id(doc_id)
        doc = get_milvus_client().get_entity_by_id(
            self.model_collection_id, ids=[int_id])[0]

        if doc is None:
            raise ValueError(
                f'Document id `{doc_id}` not found in the vector index `{self.model_collection_id}`.')

        doc_vec = np.array(doc.embedding)
        return doc_vec

    def get_similar_docs_by_doc_id(self, doc_id, topn=10, duplicate_threshold=0.999, show_duplicates=False, serialize=False, metric_type="IP"):
        self.check_wvecs()

        doc_vec = self.get_milvus_doc_vector_by_doc_id(doc_id)
        topk = 2 * topn
        dsl = get_embedding_dsl(doc_vec,
                                topk, vector_field_name=self.milvus_vector_field_name, metric_type=metric_type)
        results = get_milvus_client().search(self.model_collection_id, dsl)

        entities = results[0]
        payload = []

        for rank, ent in enumerate(entities, 1):
            if not show_duplicates:
                if ent.distance > duplicate_threshold:
                    continue

            payload.append({'id': self.get_doc_id_from_int_id(ent.id), 'score': float(np.round(
                ent.distance, decimals=5)), 'rank': rank})

            if len(payload) == topn:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_similar_words_by_doc_id(self, doc_id, topn=10, serialize=False, metric="cosine_similarity"):
        self.check_wvecs()
        buffer_topn = 2 * topn

        doc_vec = self.get_milvus_doc_vector_by_doc_id(doc_id).reshape(1, -1)

        if cosine_similarity.__name__ == metric:
            sim = cosine_similarity(doc_vec, self.word_vectors).flatten()
            argidx = sim.argsort()[-buffer_topn:][::-1]
        elif euclidean_distances.__name__ == metric:
            sim = euclidean_distances(doc_vec, self.word_vectors).flatten()
            argidx = sim.argsort()[:buffer_topn]
        else:
            raise ValueError(f"Unknow metric: `{metric}")

        payload = []
        rank = 1
        for ix, top_sim_ix in enumerate(argidx, 1):
            word = self.index2word[top_sim_ix]
            if word in stopwords.noise_words:
                continue
            payload.append({'word': word, 'score': float(np.round(
                sim[top_sim_ix], decimals=5)), 'rank': rank})

            rank += 1
            if rank > topn:
                break

        payload = sorted(payload, key=lambda x: x['rank'])
        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

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

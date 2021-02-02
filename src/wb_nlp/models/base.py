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


class BaseModel:
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

    def log(self, message):

        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def set_model_specific_attributes(self):
        pass

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

    def set_processed_corpus_id(self):
        if self.model_name in ["lda", "mallet"]:

            self.dictionary_params = self.model_config['dictionary_config']
            processed_corpus_ids = [self.cleaned_corpus_id,
                                    self.dictionary_params['dictionary_config_id']]
            self.processed_corpus_id = "_".join(processed_corpus_ids)

            self.dictionary_file = self.cleaned_docs_dir / \
                f"dictionary-{self.processed_corpus_id}.gensim.dict"
            self.corpus_path = self.cleaned_docs_dir / \
                f"bow_corpus-{self.processed_corpus_id}.mm"
        elif self.model_name == "word2vec":
            self.processed_corpus_id = self.cleaned_corpus_id

    def validate_and_prepare_requirements(self):
        self.cleaned_docs_dir = Path(dir_manager.get_data_dir(
            "corpus", "cleaned", self.cleaning_config_id))

        assert self.cleaned_docs_dir.exists()

        self.cleaned_corpus_id = get_cleaned_corpus_id(self.cleaned_docs_dir)

        model_configs_collection = mongodb.get_model_configs_collection()
        self.model_config = model_configs_collection.find_one(
            {"_id": self.model_config_id})

        # Do this to make sure that the config is consistent with the expected schema.
        self.model_config_type(**self.model_config)

        self.model_name = self.model_config["meta"]["model_name"]

        assert self.model_name == self.expected_model_name
        assert gensim.__version__ == self.model_config['meta']['library_version']

        self.dim = self.model_config[f"{self.model_name}_config"]["num_topics"]
        self.set_processed_corpus_id()

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

    def get_training_corpus(self):
        """
        This method returns a transformed corpus that can be used to train the model.
        This is specifically designed to dump the transformed corpus to disk and load it if available.
        There is an implicit assumption that the compute resources is large enough to handle the data.
        """
        if self.model_name in ["lda", "mallet"]:
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

            self.g_dict = g_dict
        elif self.model_name == "word2vec":
            corpus = MultiDirGenerator(
                base_dir=self.cleaned_docs_dir,
                source_dir_name='',
                split=True,
                min_tokens=0,
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
            # Make sure that the dimensionality uses the one in the trained model.
            if self.dim != self.model.num_topics:
                print(
                    'Warning: dimension declared is not aligned with loaded model. Using loaded model dim.')
                self.dim = self.model.num_topics

    def save_model(self):
        self.check_model()
        model_runs_info_collection = mongodb.get_model_runs_info_collection()

        if not self.model_file_name.exists():
            model_runs_info_collection.delete_one(
                {"_id": self.model_run_info["model_run_info_id"]})

            if not self.model_file_name.parent.exists():
                self.model_file_name.parent.mkdir(parents=True)

        model_file_name = str(self.model_file_name)
        self.model.save(model_file_name)

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

            self.g_dict = Dictionary()
            self.g_dict.id2token = self.model.id2word
            self.g_dict.token2id = {k: v for v,
                                    k in self.g_dict.id2token.items()}

        except FileNotFoundError:
            self.model = None

    def get_model_params(self):
        params = dict(self.model_config[f"{self.model_name}_config"])
        params.pop(f'{self.model_name}_config_id')

        if self.model_name in ["lda", "mallet"]:
            params['id2word'] = dict(self.g_dict.id2token)

        return params

    def train_model(self, retrain=False):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.
        if self.model_file_name.exists():
            print(
                'Warning: A model with the same configuration is available on disk. Loading...')
            self.load_model()
        elif self.model is None or retrain:
            corpus = self.get_training_corpus()
            params = self.get_model_params()

            self.model = self.model_class(corpus, **params)

            self.drop_milvus_collection()

            self.save()

        else:
            print('Warning: Model already trained. Not doing anything...')

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

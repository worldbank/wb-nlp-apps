'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import logging
from gensim.models import Word2Vec
import numpy as np

from wb_nlp.interfaces.milvus import (
    get_milvus_client,
)
from wb_nlp.types.models import Word2VecModelConfig, ModelTypes

from wb_nlp.models.base import BaseModel
from wb_nlp.utils.scripts import (
    configure_logger,
)


class Word2VecModel(BaseModel):
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class=Word2Vec,
        model_config_type=Word2VecModelConfig,
        expected_model_name=ModelTypes.word2vec.value,
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

    def combine_word_vectors(self, word_vecs):
        return word_vecs.mean(axis=0).reshape(1, -1)

    def transform_doc(self, document, normalize=True, tolist=False):
        # document: cleaned string

        self.check_model()
        success = True

        try:
            tokens = [i for i in document.split() if i in self.model.wv.vocab]
            word_vecs = self.model.wv[tokens]
            doc_vec = self.combine_word_vectors(word_vecs)

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

    from wb_nlp.models import word2vec_base

    # doc_fnames = list(Path('./data/raw/sample_data/TXT_ORIG').glob('*.txt'))
    # doc_ids = [hashlib.md5(p.name.encode('utf-8')).hexdigest()[:15]
    #            for p in doc_fnames]
    # corpus = ['WB'] * len(doc_ids)

    # doc_df = pd.DataFrame()
    # doc_df['id'] = doc_ids
    # doc_df['corpus'] = corpus
    # doc_df['text'] = [open(fn, 'rb').read().decode(
    #     'utf-8', errors='ignore') for fn in doc_fnames]

    wvec_model = word2vec_base.Word2VecModel(
        model_config_id="702984027cfedde344961b8b9461bfd3",
        cleaning_config_id="23f78350192d924e4a8f75278aca0e1c",
        raise_empty_doc_status=False,
        log_level=logging.DEBUG,
    )
    # %time
    wvec_model.train_model()
    # Do this if the model is available in disk but the model_run_info is not. This is to dump the model_run_info to db in case it's not present.
    # wvec_model.save()

    wvec_model.build_doc_vecs(pool_workers=3)
    print(wvec_model.get_similar_words('bank'))
    print(wvec_model.get_similar_documents('bank'))
    print(wvec_model.get_similar_docs_by_doc_id(doc_id='wb_725385'))
    print(wvec_model.get_similar_words_by_doc_id(doc_id='wb_725385'))

    # wvec_model.drop_milvus_collection()

'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import zipfile as zf
from datetime import datetime
from pathlib import Path
import json
import logging
import pandas as pd
from gensim.models.wrappers import LdaMallet
from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
from gensim import matutils
import numpy as np
from sklearn.decomposition import PCA
from wb_nlp.interfaces.milvus import (
    get_milvus_client, get_embedding_dsl
)
from wb_nlp.interfaces import mongodb
from wb_nlp import dir_manager
from wb_nlp.types.models import MalletModelConfig, ModelTypes
from wb_nlp.utils.scripts import (
    configure_logger,
)
from wb_nlp.models.lda_base import LDAModel


def transform_dt(dt):
    # Adapted from prepare-data (https://github.com/agoldst/dfr-browser/blob/master/bin/prepare-data)
    # topic x doc matrix

    D = len(dt[0])
    p = [0]
    i = []
    x = []
    p_cur = 0
    for topic_docs in dt:
        for d in range(D):
            if topic_docs[d] != 0:
                i.append(int(d))
                x.append(int(topic_docs[d]))
                p_cur += 1
        p.append(int(p_cur))

    # x -> weight
    # i -> document
    # p -> bound (p[t+1] - p[t] = # of docs in topic)

    return({"i": i, "p": p, "x": x})


class MalletModel(LDAModel):
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class=LdaMallet,
        model_config_type=MalletModelConfig,
        expected_model_name=ModelTypes.mallet.value,
        model_run_info_description="",
        raise_empty_doc_status=True,
        log_level=logging.WARNING,
    ):
        configure_logger(log_level)
        self.log_level = log_level
        self.logger = logging.getLogger(__file__)

        self.cleaning_config_id = cleaning_config_id
        self.model_config_id = model_config_id
        self.model_class = model_class  # Example: LdaMallet
        self.model_config_type = model_config_type  # Example: MalletModelConfig
        self.expected_model_name = expected_model_name
        self.model_run_info_description = model_run_info_description

        self.validate_and_prepare_requirements()

        self.model = None
        self.raise_empty_doc_status = raise_empty_doc_status

        # Try to load the model
        self.load()
        self.set_model_specific_attributes()

        self.create_milvus_collection()
        self.topic_composition_ranges = None

    def train_model(self, retrain=False):
        # TODO: Add a way to augment the content of the docs
        # with an external dataset without metadata.
        if self.model_file_name.exists() and not retrain:
            self.log(
                'Warning: A model with the same configuration is available on disk. Loading...')
            self.load_model()
        elif self.model is None or retrain:
            self.log(
                'Starting model training...')
            corpus = self.get_training_corpus()
            params = self.get_model_params()

            prefix = Path(dir_manager.get_path_from_root(params['prefix']))

            # models/mallet/tmp/tmp_
            params["prefix"] = f"{prefix}{self.model_run_info['model_run_info_id']}_"

            self.mallet_model = self.model_class(corpus=corpus, **params)

            self.model = malletmodel2ldamodel(
                self.mallet_model, gamma_threshold=0.001, iterations=self.mallet_model.iterations)
            self.model.minimum_probability = 0.001
            self.model.id2word = self.mallet_model.id2word

            self.drop_milvus_collection()

            self.extract_dfr_data()
            self.save()

        else:
            self.log('Warning: Model already trained. Not doing anything...')

    def get_mallet_topic(self, topicid, topn=10, normalize=True):
        """Get `topn` most probable words for the given `topicid`.
        Parameters
        ----------
        topicid : int
            Id of topic.
        topn : int, optional
            Top number of topics that you'll receive.
        Returns
        -------
        list of (str, float)
            Sequence of probable words, as a list of `(word, token_count)` for `topicid` topic.
        """

        topic = self.mallet_model.word_topics[topicid]

        if normalize:
            topic = topic / topic.sum()  # normalize to probability dist

        bestn = matutils.argsort(topic, topn, reverse=True)
        beststr = [(self.mallet_model.id2word[idx], topic[idx])
                   for idx in bestn]
        return beststr

    def get_tw(self, mallet_model, n=50):
        topic_weights = []

        for i in range(mallet_model.num_topics):
            words, weights = zip(
                *self.get_mallet_topic(i, topn=n, normalize=False))
            topic_weights.append(
                dict(words=list(words), weights=list(weights)))

        # alpha = [mallet_model.topic_threshold] * \
        #     mallet_model.num_topics
        alpha = list(mallet_model.alpha)

        return dict(alpha=alpha, tw=topic_weights)

    def scale_topics(self, word_topics):
        return PCA(n_components=2, random_state=1029).fit_transform(word_topics)

    def extract_dfr_data(self):

        self.dfr_data_dir = Path(dir_manager.get_path_from_root(
            "models", "dfr", "data", self.model_run_info["model_run_info_id"]))

        dt = pd.read_csv(
            self.mallet_model.fdoctopics(), delimiter='\t', header=None,
            names=[i for i in range(self.mallet_model.num_topics)], index_col=None,
            usecols=[i + 2 for i in range(self.mallet_model.num_topics)],
        )

        dt.index = self.corpus_ids
        # Make sure weights are normalized per document.
        dt = dt.divide(dt.sum(axis=1), axis=0)

        # Get tokens attributed to topic.
        dt = dt.multiply(self.corpus_token_counts, axis=0).round(0).astype(int)

        self.logger.info('Generating dfr-browser data...')
        ddt = transform_dt(dt.values.T)
        ttw = self.get_tw(self.mallet_model)

        # docs_metadata = mongodb.get_docs_metadata_collection()
        docs_metadata = mongodb.get_collection(
            db_name="test_nlp", collection_name="docs_metadata")
        meta = docs_metadata.find({"id": {"$in": self.corpus_ids}}, projection=[
                                  "id", "title", "author", "year", "corpus"])
        meta_df = []
        for m in meta:
            e = [""] * 9
            e[0] = m["id"]
            e[1] = m["title"]
            e[2] = ",".join(m["author"]) if m["author"] else ""
            e[3] = m["corpus"]
            e[6] = m["year"]
            meta_df.append(e)
        meta_df = pd.DataFrame(meta_df)

        meta_df.to_csv(
            self.dfr_data_dir / "meta.csv.zip",
            compression=dict(method='zip', archive_name='meta.csv'),
            index=None, header=None)

        if not self.dfr_data_dir.exists():
            self.dfr_data_dir.mkdir(parents=True)

        with open(self.dfr_data_dir / 'tw.json', 'w') as open_fl:
            json.dump(ttw, open_fl)

        with open(self.dfr_data_dir / 'dt.json', 'w') as open_fl:
            json.dump(ddt, open_fl)

        with zf.ZipFile(self.dfr_data_dir / 'dt.json.zip', "w") as zip_file:
            zip_file.write(self.dfr_data_dir / 'dt.json', 'dt.json')

        scaled_topics = self.scale_topics(self.mallet_model.word_topics)
        scaled_topics = pd.DataFrame(scaled_topics)
        scaled_topics.to_csv(self.dfr_data_dir /
                             'topic_scaled.csv', index=None, header=None)

        info_json = {
            "title": f"Topics of model id {self.model_run_info['model_run_info_id']}<\/em>",
            "meta_info": "This site is the working demo for <a href=\"/\">dfr-browser</a>, a browsing interface for topic models of journal articles or other text.",
            "VIS": {
                "condition": {
                    "type": "time",
                    "spec": {
                        "field": "date",
                        "unit": "year",
                        "n": 1
                    }
                },
                "bib": {
                    "author": {
                        "author_delimeter": ","
                    }
                },
                "bib_sort": {
                    "major": "year",
                    "minor": "alpha"
                },
                "model_view": {
                    "plot": {
                        "words": 6,
                        "size_range": [6, 14]
                    }
                }
            }
        }

        with open(self.dfr_data_dir / 'info.json', 'w') as fl:
            json.dump(info_json, fl)


if __name__ == '__main__':
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
    %time wvec_model.train_model()

    wvec_model.build_doc_vecs(pool_workers=3)
    wvec_model.get_similar_words('bank')
    wvec_model.get_similar_documents('bank')
    wvec_model.get_similar_docs_by_id(doc_id='8314385c25c7c5e')
    wvec_model.get_similar_words_by_id(doc_id='8314385c25c7c5e')
    """
    import logging
    from wb_nlp.models import mallet_base

    # rm data/corpus/cleaned/23f78350192d924e4a8f75278aca0e1c/bow_corpus-531c1e4f358efbc07b97a58815558c53_5a80eb483f11c3b899d8cba7237215f9.mm*
    # rm data/corpus/cleaned/23f78350192d924e4a8f75278aca0e1c/dictionary-531c1e4f358efbc07b97a58815558c53_5a80eb483f11c3b899d8cba7237215f9.gensim.dict
    # rm -rf models/lda/5ac7fd8a83c6bc5fce480323eb01d137

    mallet_model = mallet_base.MalletModel(
        model_config_id="5e26b5090bdd91d7aee4e5e89753a33b",
        cleaning_config_id="23f78350192d924e4a8f75278aca0e1c",
        model_class=LdaMallet,
        model_config_type=MalletModelConfig,
        expected_model_name="mallet",
        raise_empty_doc_status=False, log_level=logging.DEBUG)
    # %time
    mallet_model.train_model(retrain=True)
    # Do this if the model is available in disk but the model_run_info is not. This is to dump the model_run_info to db in case it's not present.
    # mallet_model.save()

    mallet_model.build_doc_vecs(pool_workers=3)
    print(mallet_model.get_similar_words('bank'))
    print(mallet_model.get_similar_documents('bank'))
    print(mallet_model.get_similar_docs_by_doc_id(doc_id='wb_725385'))
    print(mallet_model.get_similar_words_by_doc_id(doc_id='wb_725385'))

    # mallet_model.drop_milvus_collection()

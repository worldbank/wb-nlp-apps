'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
import logging
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.cluster import KMeans
import networkx as nx
import graph_tool.all as gt
import pyintergraph
from wb_nlp.graph.graph_interface import FixedInterGraph
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

    def get_similar_words_graph(self, document, topn=10, edge_thresh=0.5, n_clusters=5, serialize=False, metric="cosine_similarity"):

        words = []
        word_ids = []

        for result in self.get_similar_words(
                document, topn=topn, serialize=False, metric=metric):
            words.append(result["word"])
            word_ids.append(result["id"])
            print(result)

        related_words = []
        for word in words:
            for result in self.get_similar_words(
                    word, topn=topn, serialize=False, metric=metric):
                if result["word"] in words or result["word"] in related_words:
                    continue
                related_words.append(result["word"])
                word_ids.append(result["id"])

        words.extend(related_words)

        # words_set = [{document: self.get_similar_words(
        #     document, topn=topn, serialize=False, metric=metric)}]
        # words_set.extend([{result["word"]: self.get_similar_words(
        #     result["word"], topn=topn, serialize=False, metric=metric)} for result in words_set[0][document]])

        word_vectors = self.word_vectors[word_ids]
        sim = cosine_similarity(word_vectors, word_vectors)
        # sim[sim < edge_thresh] = 0
        graph_df = pd.DataFrame(sim, index=words, columns=words)
        # graph_df[graph_df < edge_thresh] = 0

        cluster = KMeans(n_clusters=n_clusters)
        cluster.fit(word_vectors)
        word_clusters = cluster.predict(word_vectors)

        nx_graph = nx.from_pandas_adjacency(graph_df)
        centrality = nx.pagerank(nx_graph)
        # centrality = nx.eigenvector_centrality(nx_graph)

        inter_graph = FixedInterGraph.from_networkx(nx_graph)
        # inter_graph.node_labels
        gt_graph = inter_graph.to_graph_tool()
        nodes_pos = gt.sfdp_layout(gt_graph)

        # # G = pd.DataFrame(np.random.random(size=(30, 30)))
        # # G[G < 0.2] = 0
        # # G.columns = G.columns.astype(str).map(lambda x: f"node_{x}")
        # # G.index = G.index.astype(str).map(lambda x: f"node_{x}")
        # # G = nx.from_pandas_adjacency(G)

        # # GG = FixedInterGraph.from_networkx(G)
        # # GG.edge_attributes = [{"weight": [ea["weight"]]} for ea in GG.edge_attributes]
        # # gt_graph = GG.to_graph_tool()
        # # pos = gt.sfdp_layout(gt_graph)

        nodes = []
        links = [{"source": l[0], "target": l[1]} for l in nx_graph.edges]
        categories = [{"name": f"cluster {i + 1}"} for i in range(n_clusters)]

        for word, word_id, cluster_id, pos in zip(words, word_ids, word_clusters, nodes_pos):
            nodes.append(
                dict(
                    id=word_id,
                    name=word,
                    symbolSize=centrality[word],
                    x=pos[0],
                    y=pos[1],
                    value=centrality[word],
                    category=cluster_id,
                )
            )

        # { "nodes": [
        # {
        # "id": "60",
        # "name": "Prouvaire",
        # "symbolSize": 17.295237333333333,
        # "x": 614.29285,
        # "y": -69.3104,
        # "value": 25.942856,
        # "category": 8
        # },], "links": [
        # {
        # "source": "1",
        # "target": "0"
        # },], "categories": [{"name": "cat_name"},]}

        # return payload

        return dict(nodes=nodes, links=links, categories=categories)


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
    wvec_model.train_model()  # retrain=True)
    # Do this if the model is available in disk but the model_run_info is not. This is to dump the model_run_info to db in case it's not present.
    # wvec_model.save()

    wvec_model.build_doc_vecs(pool_workers=3)
    print(wvec_model.get_similar_words('bank'))
    print(wvec_model.get_similar_documents('bank'))
    print(wvec_model.get_similar_docs_by_doc_id(doc_id='wb_725385'))
    print(wvec_model.get_similar_words_by_doc_id(doc_id='wb_725385'))

    # wvec_model.drop_milvus_collection()

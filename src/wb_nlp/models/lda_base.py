'''This module implements the word2vec model service that is responsible
for training the model as well as a backend interface for the API.
'''
from datetime import datetime
import json
import logging
import pandas as pd
from gensim.models.ldamulticore import LdaMulticore

import numpy as np

from wb_nlp.interfaces.milvus import (
    get_milvus_client, get_embedding_dsl
)
from wb_nlp.interfaces import mongodb, elasticsearch

from wb_nlp.types.models import LDAModelConfig, ModelTypes
from wb_nlp.utils.scripts import (
    configure_logger,
)
from wb_nlp.models.base import BaseModel


class LDAModel(BaseModel):
    def __init__(
        self,
        model_config_id,
        cleaning_config_id,
        model_class=LdaMulticore,
        model_config_type=LDAModelConfig,
        expected_model_name=ModelTypes.lda.value,
        model_run_info_description="",
        model_run_info_id=None,
        raise_empty_doc_status=True,
        log_level=logging.INFO,
    ):

        super().__init__(
            model_config_id=model_config_id,
            cleaning_config_id=cleaning_config_id,
            model_class=model_class,
            model_config_type=model_config_type,
            expected_model_name=expected_model_name,
            model_run_info_description=model_run_info_description,
            model_run_info_id=model_run_info_id,
            raise_empty_doc_status=raise_empty_doc_status,
            log_level=log_level,
        )

        self.topic_composition_ranges = None

        try:
            self.logger.info("Initializing topic composition")
            self.get_topic_composition_ranges()
            self.logger.info("Finished initializing topic composition")
        except ValueError:
            self.logger.info("Skipping initialization of topic composition")

    def set_model_specific_attributes(self):
        self.num_topics = self.dim

    def transform_doc(self, document, normalize=True, tolist=False):
        # This function is the primary method of converting a document
        # into its vector representation based on the model.
        # This should be implemented in the respective models.
        # The expected output is a dictionary with keys:
        # - doc_vec  # numpy array of shape (1, self.dim)
        # - success  # Whether the transformation went successfully
        self.check_model()
        success = True

        document = document.lower()

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

        if tolist:
            doc_vec = doc_vec.ravel().tolist()

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
        # print(found_topics)
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
        for topic_id in range(self.model.num_topics):
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

    def _mdb_get_docs_by_topic_composition(self, topic_percentage, return_all_topics=False):
        self.check_wvecs()
        model_run_info_id = self.model_run_info["model_run_info_id"]

        doc_topic_collection = mongodb.get_document_topics_collection()

        topic_cols = [f"topic_{id}" for id in sorted(topic_percentage)]
        topic_filters = {f"topics.topic_{id}": {"$gte": val}
                         for id, val in sorted(topic_percentage.items())}
        topic_filters = {
            "model_run_info_id": model_run_info_id, **topic_filters}
        cands = doc_topic_collection.find(topic_filters)

        doc_df = pd.DataFrame(cands)

        if doc_df.empty:
            return doc_df

        doc_df = doc_df.set_index(
            "id")["topics"].apply(pd.Series)

        if not return_all_topics:
            doc_df = doc_df[topic_cols]

        doc_df = doc_df.round(5)

        return doc_df

    def _get_docs_by_topic_composition_search(self, topic_percentage):
        model_run_info_id = self.model_run_info["model_run_info_id"]

        search = elasticsearch.DocTopic.search()

        topic_filters = [dict(range={f"topics.topic_{id}": {"gte": val}})
                         for id, val in sorted(topic_percentage.items())]
        search = search.query(
            dict(
                bool=dict(
                    must=[
                        {"term": {"model_run_info_id": model_run_info_id}}] + topic_filters
                )
            )
        )
        return search

    def _get_docs_by_topic_composition(self, topic_percentage, return_all_topics=False):
        self.check_wvecs()

        search = self._get_docs_by_topic_composition_search(topic_percentage)
        topic_cols = [f"topic_{id}" for id in sorted(topic_percentage)]

        search = search[0: search.count()]
        response = search.execute()

        doc_df = pd.DataFrame([h.to_dict() for h in response.hits])

        if doc_df.empty:
            return doc_df

        doc_df = doc_df.set_index(
            "id")["topics"].apply(pd.Series)

        if not return_all_topics:
            doc_df = doc_df[topic_cols]

        doc_df = doc_df.round(5)

        return doc_df

    def get_docs_by_topic_composition_count(self, topic_percentage):
        search = self._get_docs_by_topic_composition_search(topic_percentage)
        return search.count()

        # return len(self._get_docs_by_topic_composition(topic_percentage))

    def get_docs_by_topic_composition(self, topic_percentage, serialize=False, from_result=0, size=10, return_all_topics=False):
        '''
        topic_percentage (dict): key (int) corresponds to topic id and value (float [0, 1]) corresponds to the expected topic percentage.
        '''

        # topic_percentage = {6: 0.1, 42: 0.1}

        doc_df = self._get_docs_by_topic_composition(
            topic_percentage, return_all_topics=return_all_topics)
        doc_count = len(doc_df)
        payload = []

        if doc_count > 0:

            doc_rank = (-1 * doc_df
                        ).rank().mean(axis=1).rank().sort_values()
            doc_rank.name = "rank"
            doc_rank = doc_rank.reset_index().to_dict("records")
            doc_topic = doc_df.T.to_dict()

            for rank, ent in enumerate(doc_rank):

                if from_result > rank:
                    continue

                payload.append(
                    {'id': ent["id"], 'topic': doc_topic[ent["id"]], 'rank': rank + 1})

                if len(payload) == size:
                    break

            payload = sorted(payload, key=lambda x: x['rank'])
            if serialize:
                payload = pd.DataFrame(payload).to_json()

        return dict(total=doc_count, hits=payload)

    def mdb_get_topic_composition_ranges(self, serialize=False):
        self.check_wvecs()

        if self.topic_composition_ranges is None:
            model_run_info_id = self.model_run_info["model_run_info_id"]
            doc_topic_collection = mongodb.get_document_topics_collection()

            self.topic_composition_ranges = pd.DataFrame([
                list(doc_topic_collection.aggregate([
                    {"$match": {"model_run_info_id": model_run_info_id}},
                    {"$group": {
                        "_id": f"topic_{i}",
                        "min": {"$min": f"$topics.topic_{i}"},
                        "max": {"$max": f"$topics.topic_{i}"}}}]))[0] for i in range(self.dim)
            ]).rename(columns={"_id": "topic"}).set_index("topic").T.to_dict()  # "records")

        # Data structure: {topic_id: {min: <min_val>, max: <max_val>}}
        payload = self.topic_composition_ranges

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_topic_composition_ranges(self, serialize=False):
        self.check_wvecs()

        if self.topic_composition_ranges is None:
            model_run_info_id = self.model_run_info["model_run_info_id"]

            topic_stats = []
            for i in range(self.dim):
                search = elasticsearch.DocTopic.search()
                query_body = dict(
                    aggs={f"topic_{i}": dict(
                        stats=dict(field=f"topics.topic_{i}"))},
                    query=dict(
                        term=dict(model_run_info_id=model_run_info_id)),
                    size=0
                )

                search.update_from_dict(query_body)
                result = search.execute()
                topic_stats.append(result.aggregations.to_dict())

            self.topic_composition_ranges = {
                k: v for i in topic_stats for k, v in i.items()
            }

        # Data structure: {topic_id: {min: <min_val>, max: <max_val>}}
        payload = self.topic_composition_ranges

        if serialize:
            payload = pd.DataFrame(payload).to_json()

        return payload

    def get_topic_share(self, topic_id: int, doc_ids: list):
        model_run_info_id = self.model_run_info["model_run_info_id"]
        doc_topic_collection = mongodb.get_document_topics_collection()

        normed_docs_topic = doc_topic_collection.find(
            {"id": {"$in": doc_ids}, "model_run_info_id": model_run_info_id}, projection=["id", f"topics.topic_{topic_id}"])
        normed_docs_topic = pd.DataFrame(list(normed_docs_topic))[
            ["id", "topics"]]
        normed_docs_topic["topics"] = normed_docs_topic["topics"].apply(
            pd.Series)
        topic_share = normed_docs_topic.set_index('id')["topics"].to_dict()

        return topic_share

    def get_partition_topic_share(self, topic_id: int, adm_regions: list, major_doc_types: list, year_start: int = 1950, year_end: int = datetime.now().year, return_records=True):
        # docs_metadata = mongodb.get_docs_metadata_collection()
        docs_metadata = mongodb.get_collection(
            db_name="test_nlp", collection_name="docs_metadata")

        major_doc_types_data = {}
        adm_regions_data = {}

        for part in major_doc_types:
            data_iterator = docs_metadata.find(
                filter={'major_doc_type': part}, projection=['id', 'year'])

            data = pd.DataFrame(list(data_iterator)).set_index('id')

            topic_share = pd.Series(self.get_topic_share(
                topic_id, data.index.tolist()))
            data['topic_share'] = topic_share

            data.year = data.year.replace('', np.nan)
            data = data.dropna(subset=['year'])

            data.year = data.year.astype(int)
            data = data[data.year.between(year_start, year_end)]

            data = data.groupby('year')['topic_share'].sum()

            if return_records:
                major_doc_types_data[part] = data.reset_index().to_dict(
                    'records')
            else:
                major_doc_types_data[part] = data.to_dict()

        for part in adm_regions:
            data_iterator = docs_metadata.find(
                filter={'adm_region': part}, projection=['id', 'year'])
            data = pd.DataFrame(list(data_iterator)).set_index('id')

            topic_share = pd.Series(self.get_topic_share(
                topic_id, data.index.tolist()))
            data['topic_share'] = topic_share

            data.year = data.year.replace('', np.nan)
            data = data.dropna(subset=['year'])

            data.year = data.year.astype(int)
            data = data[data.year.between(year_start, year_end)]
            data = data.groupby('year')['topic_share'].sum()

            if return_records:
                adm_regions_data[part] = data.reset_index().to_dict('records')
            else:
                adm_regions_data[part] = data.to_dict()

        payload = {}
        payload.update(major_doc_types_data)
        payload.update(adm_regions_data)

        return {'topic_shares': payload, 'topic_words': self.get_topic_words(topic_id)}

    def get_topic_profile_data_payload(self, df, field, type="line"):
        x = sorted(df.index)
        legend = sorted(df.columns)
        series = [dict(name=f, data=df.loc[x, f].tolist(),
                       stack=field, type=type, areaStyle={}) for f in legend]
        return dict(
            year=x,
            series=series,
            legend=legend,
        )

    def get_topic_profile_by_field(self, field, topic_id, type="line"):
        topic_agg = elasticsearch.DocTopicAggregations(model_id=self.model_id)

        data = pd.DataFrame(topic_agg.get_topic_profile_by_year_by_field(
            field=field,
            topic=f"topic_{topic_id}",
            filters=[{"term": {"corpus": "WB"}}]))

        year_field_topic_sum_df = data.pivot(
            index="year", columns=field, values=f"{field}_topic_sum").fillna(0)
        year_doc_count_df = data.pivot(
            index="year", columns=field, values="year_doc_count").fillna(0)

        normed_year_field_topic_sum_df = (
            year_field_topic_sum_df / year_doc_count_df).fillna(0)

        topic_volume = self.get_topic_profile_data_payload(
            year_field_topic_sum_df, field=field, type=type)
        topic_share = self.get_topic_profile_data_payload(
            normed_year_field_topic_sum_df, field=field, type=type)

        return dict(
            field=field,
            topic=f"topic_{topic_id}",
            volume=topic_volume,
            share=topic_share
        )

    def get_full_topic_profile(self, topic_id: int, type="line"):

        data_adm_region = self.get_topic_profile_by_field(
            field="adm_region", topic_id=topic_id, type=type)
        data_major_doc_type = self.get_topic_profile_by_field(
            field="major_doc_type", topic_id=topic_id, type=type)

        return dict(adm_region=data_adm_region, major_doc_type=data_major_doc_type)

    def get_full_topic_profiles(self, topic_id: int, year_start: int = 1950, year_end: int = datetime.now().year, type="line", return_records=True):
        # docs_metadata = mongodb.get_docs_metadata_collection()

        data = self.get_full_topic_profile(topic_id=topic_id, type=type)

        data['topic_words'] = self.get_topic_words(topic_id)

        return data


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
    # Do this if the model is available in disk but the model_run_info is not. This is to dump the model_run_info to db in case it's not present.
    # lda_model.save()

    lda_model.drop_milvus_collection()

    lda_model.build_doc_vecs(pool_workers=3)
    print(lda_model.get_similar_words('bank'))
    print(lda_model.get_similar_documents('bank'))
    print(lda_model.get_similar_docs_by_doc_id(doc_id='wb_725385'))
    print(lda_model.get_similar_words_by_doc_id(doc_id='wb_725385'))

    # lda_model.drop_milvus_collection()

    # lda_model = lda_base.LDAModel(
    #     model_config_id="ef0ab0459e9c28de8657f3c4f5b2cd86",
    #     cleaning_config_id="23f78350192d924e4a8f75278aca0e1c",
    #     model_run_info_id="3e82ec784f125709c8bac46d7dd8a67f")

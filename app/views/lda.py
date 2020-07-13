### WORD2VEC
import path_manager
import os
import glob
import requests
import json
import numpy as np
import pandas as pd
from flask_restful import Resource, reqparse
from flask_restful.inputs import boolean
from services.lda_module import LDAInferencer
from views.cleaning import clean_text
from services.metadata import get_document_metadata, get_data_iterator
import werkzeug
from flask import request
from datetime import datetime

import uuid
import shutil

import pylab as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import time

from utils.parser import parse_args

headers = {"Content-Type": "application/json", "Accept": "application/json"}
cleaning_url = 'http://localhost:8910/api/clean_text'
LDA_MODELS_PATH = path_manager.get_models_path('LDA')
LDA_MODELS = {}

def load_model(corpus_id, model_id):
    # No doc_df for now.

    lda_model = LDAInferencer(corpus_id=corpus_id, model_id=model_id)

    return lda_model


def get_model(corpus_id, model_id):
    if corpus_id not in LDA_MODELS:
        LDA_MODELS[corpus_id] = {model_id: load_model(corpus_id, model_id)}
    else:
        if model_id not in LDA_MODELS[corpus_id]:
            LDA_MODELS[corpus_id][model_id] = load_model(corpus_id, model_id)

    return LDA_MODELS.get(corpus_id, {}).get(model_id)


parser_lda = reqparse.RequestParser()
parser_lda.add_argument(
    'id', type=str,
    required=False, help='Valid id of document in corpus.'
)
parser_lda.add_argument(
    'raw_text', type=str,
    required=False, help='raw text input required'
)
parser_lda.add_argument(
    'file', type=werkzeug.datastructures.FileStorage,
    location='files',
    required=False, help='File to upload.'
)
parser_lda.add_argument(
    'topn', type=int, default=10,
    required=False, help='Return at most topn documents.'
)
parser_lda.add_argument(
    'corpus_id', type=str, default='WB',
    required=False, help='Corpus used to train the word2vec model.'
)
parser_lda.add_argument(
    'model_id', type=str, default='ALL_100',
    required=False, help='Identification for the model defined by the corpus partition and vector dimension.'
)
parser_lda.add_argument(
    'clean_doc', type=boolean, default=True,
    required=False, help='Specifies whether cleaning should be done on the raw_text.'
)
parser_lda.add_argument(
    'use_ngram', type=boolean, default=True,
    required=False, help='Flag to choose if ngram transformed text will be used.'
)
parser_lda.add_argument(
    'show_duplicates', type=boolean, default=False,
    required=False, help='Flag that indicates whether to return highly similar or possibly duplicate documents.'
)
parser_lda.add_argument(
    'duplicate_threshold', type=float, default=0.01,
    required=False, help='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
)
parser_lda.add_argument(
    'return_related_words', type=boolean, default=True,
    required=False, help='Flag indicating an option to return similar or topic words to the document.'
)
parser_lda.add_argument(
    'topic_id', type=int, default=0,
    required=False, help='Topic id.'
)

parser_lda.add_argument(
    'topn_topics', type=int, default=10,
    required=False, help='Return at most topn topics.'
)
parser_lda.add_argument(
    'topn_words', type=int, default=10,
    required=False, help='Return at most topn_words words in topic.'
)
parser_lda.add_argument(
    'total_topic_score', type=float, default=0.8,
    required=False, help='Return at most total_topic_score cummulative proportion topics.'
)
parser_lda.add_argument(
    'total_word_score', type=float, default=0.8,
    required=False, help='Return at most total_word_score cummulative proportion words in topic.'
)
parser_lda.add_argument(
    'major_doc_types', default=[], action='append',
    required=False, help='Major doc types to compare topics.'
)
parser_lda.add_argument(
    'adm_regions', default=[], action='append',
    required=False, help='Admin regions to compare topics.'
)
parser_lda.add_argument(
    'lending_instruments', default=[], action='append',
    required=False, help='Lending instruments to compare topics.'
)
parser_lda.add_argument(
    'year_start', type=int, default=1950,
    required=False, help='Admin regions to compare topics.'
)
parser_lda.add_argument(
    'year_end', type=int, default=datetime.now().year,
    required=False, help='Admin regions to compare topics.'
)
parser_lda.add_argument(
    'return_records', type=boolean, default=True,
    required=False, help='Flag indicating the data structure to return in topic share.'
)
parser_lda.add_argument(
    'topic_percentage', type=dict, default={},
    required=False, help='Key-value pair of topic and expected percentage in a document.'
)
parser_lda.add_argument(
    'closest_to_minimum', type=boolean, default=False,
    required=False, help='This adjusts the sorting of the returned documents. If set to False, it will give the documents with the highest topic composition. If set to True, it will rank documents having topic composition closest to the given minimum.'
)


def preprocess_input(args):
    corpus_id = args['corpus_id']
    model_id = args['model_id']
    should_clean = args['clean_doc']
    topn = args['topn']
    use_ngram = args['use_ngram']

    if args.get('file') is not None:
        file = args['file']
        text = file.read()
        try:
            text = text.decode('utf-8', 'ignore')
        except:
            return {'Error': "File can't be decoded."}

    elif args.get('raw_text') is not None:
        text = args['raw_text']
    else:
        return {'Error': 'Please provide a file or a raw_text parameter.'}

    model = get_model(corpus_id, model_id)
    if model is None:
        return {'Error': f'No model found for {corpus_id}-{model_id}'}

    # Clean document first.
    if should_clean:
        text = clean_text(text)
        if not use_ngram:
            text = text.get('text')
        else:
            text = text.get('ngram_text', text.get('text'))

    return {'text': text, 'model': model, 'topn': topn}


class LDAModelInferTopics(Resource):
    def post(self):
        args = parse_args(parser_lda)

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']

        return json.loads(
            model.infer_topics(text=text, serialize=True)
        )

    def get(self):
        return self.post()


class LDAModelTopicsView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        topn_words = args['topn_words']

        model = get_model(corpus_id, model_id)

        if model is None:
            return {'Error': f'No model found for {corpus_id}-{model_id}'}

        return json.loads(
            model.get_model_topic_words(topn_words=topn_words, serialize=True)
        )

    def get(self):
        return self.post()


class LDATopicWordsView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        topic_id = args['topic_id']

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        topn_words = args['topn_words']

        model = get_model(corpus_id, model_id)

        if model is None:
            return {'Error': f'No model found for {corpus_id}-{model_id}'}

        return {'words': pd.read_json(
            model.get_topic_words(topic_id, topn_words=topn_words, serialize=True)
        ).to_dict('records')}

    def get(self):
        return self.post()


class LDADocTopicsView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']

        topn_topics = args['topn_topics']
        total_topic_score = args['total_topic_score']

        return {'topics': pd.read_json(
            model.get_doc_topic_words(text, topn_topics=topn_topics, total_topic_score=total_topic_score, serialize=True)
        ).to_dict('records')}

    def get(self):
        return self.post()


class LDADocTopicsByIDView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        id = args['id']

        topn_topics = args['topn_topics']
        total_topic_score = args['total_topic_score']

        model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        if model is None:
            return {}

        return {'topics': pd.read_json(
            model.get_doc_topic_words_by_id(id, topn_topics=topn_topics, total_topic_score=total_topic_score, serialize=True)
        ).to_dict('records')}

    def get(self):
        return self.post()


class LDARelatedDocsView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        output = preprocess_input(args)
        if 'Error' in output:
            return output

        text = output['text']
        model = output['model']
        topn = output['topn']

        show_duplicates = args['show_duplicates']
        duplicate_threshold = args['duplicate_threshold']

        payload = pd.read_json(
            model.get_similar_documents(
                text, topn=topn, serialize=True,
                duplicate_threshold=duplicate_threshold,
                show_duplicates=show_duplicates,
            )
        ).to_dict('records')

        for p in payload:
            p['metadata'] = get_document_metadata(p['id'])

        return {'docs': payload}

    def get(self):
        return self.post()


class LDARelatedDocsByIDView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        id = args['id']
        topn = args['topn']
        show_duplicates = args['show_duplicates']
        duplicate_threshold = args['duplicate_threshold']
        return_related_words = args['return_related_words']

        model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)
        if model is None:
            return {}

        payload = pd.read_json(
            model.get_similar_docs_by_id(
                id, topn=topn, serialize=True,
                duplicate_threshold=duplicate_threshold,
                show_duplicates=show_duplicates,
            )
        ).to_dict('records')

        for p in payload:
            p['metadata'] = get_document_metadata(p['id'])

        return {'docs': payload}

    def get(self):
        return self.post()


class LDAPartitionTopicShare(Resource):
    def post(self):
        args =parse_args(parser_lda)

        year_start = args['year_start']
        year_end = args['year_end']

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        topic_id = args['topic_id']
        return_records = args['return_records']

        model = get_model(corpus_id, model_id)  # WVEC_MODELS.get(corpus_id, {}).get(model_id)

        major_doc_types = args['major_doc_types']
        adm_regions = args['adm_regions']
        lending_instruments = args['lending_instruments']

        major_doc_types_data = {}
        adm_regions_data = {}
        lending_instruments_data = {}
        plot_data = {}

        for part in lending_instruments:
            data_iterator = get_data_iterator(filter={'wb_lending_instrument': {'$regex': f'{part}', '$options': 'i'}}, projection=['_id', 'year'])
            data = pd.DataFrame(list(data_iterator)).rename(columns={'_id': 'id'}).set_index('id')

            topic_share = pd.Series(model.get_topic_share(topic_id, data.index.tolist()))
            print(topic_share.shape)
            data['topic_share'] = topic_share

            data.year = data.year.replace('', np.nan)
            data = data.dropna(subset=['year'])

            data.year = data.year.astype(int)
            data = data[data.year.between(year_start, year_end)]

            data = data.groupby('year')['topic_share'].sum()

            plot_data.update({part: data.to_dict()})

            if return_records:
                lending_instruments_data[part] = data.reset_index().to_dict('records')
            else:
                lending_instruments_data[part] = data.to_dict()

        for part in major_doc_types:
            data_iterator = get_data_iterator(filter={'major_doc_type': part}, projection=['_id', 'year'])
            data = pd.DataFrame(list(data_iterator)).rename(columns={'_id': 'id'}).set_index('id')

            topic_share = pd.Series(model.get_topic_share(topic_id, data.index.tolist()))
            data['topic_share'] = topic_share

            data.year = data.year.replace('', np.nan)
            data = data.dropna(subset=['year'])

            data.year = data.year.astype(int)
            data = data[data.year.between(year_start, year_end)]

            data = data.groupby('year')['topic_share'].sum()

            plot_data.update({part: data.to_dict()})

            if return_records:
                major_doc_types_data[part] = data.reset_index().to_dict('records')
            else:
                major_doc_types_data[part] = data.to_dict()

        for part in adm_regions:
            data_iterator = get_data_iterator(filter={'adm_region': part}, projection=['_id', 'year'])
            data = pd.DataFrame(list(data_iterator)).rename(columns={'_id': 'id'}).set_index('id')

            topic_share = pd.Series(model.get_topic_share(topic_id, data.index.tolist()))
            data['topic_share'] = topic_share

            data.year = data.year.replace('', np.nan)
            data = data.dropna(subset=['year'])

            data.year = data.year.astype(int)
            data = data[data.year.between(year_start, year_end)]
            data = data.groupby('year')['topic_share'].sum()

            plot_data.update({part: data.to_dict()})

            if return_records:
                adm_regions_data[part] = data.reset_index().to_dict('records')
            else:
                adm_regions_data[part] = data.to_dict()

        payload = {}
        payload.update(major_doc_types_data)
        payload.update(adm_regions_data)
        payload.update(lending_instruments_data)

        filename = f'{uuid.uuid4()}.png'

        # self.plot_topic_share(plot_data, filename)

        return {'topic_shares': payload, 'topic_words': model.get_topic_words(topic_id), 'filename': filename}

    def get(self):
        return self.post()

    def plot_topic_share(self, payload, filename):
        df = pd.DataFrame(payload)

        figure = plt.figure(figsize=(12, 3 * df.shape[1]))

        # ymax = pd.np.round(df.max().max(), 2) + 0.005
        # for ix, part in enumerate(df.columns):
        #     ax = figure.add_subplot(int(f'{df.shape[1]}1{ix + 1}'))
        #     d = df[part].reset_index().rename(columns={'index': 'year'})

        #     if (ix + 1) < df.shape[1]:
        #         d.plot(x='year', kind='bar', ax=ax, ylim=(0, ymax))
        #         ax.xaxis.set_ticklabels([''] * d.shape[0])
        #         ax.xaxis.set_label_text('')

        #     else:
        #         d.plot(x='year', kind='bar', ax=ax, ylim=(0, ymax))

        # figure.savefig(f'/tmp/{filename}', tight_layout=True)

        df.index = pd.to_datetime(df.index)

        year_mark = 10
        ymax = pd.np.round(df.max().max(), 2) + 0.005
        axs = df.plot(kind='bar', subplots=True, figsize=(12, df.shape[1] * 3), ylim=(0, ymax))

        for ax in axs:
            ax.set_title('')

            # ticklabels = [''] * len(df)
            # skip = df.shape[0] // 5
            # ticklabels = df.reset_index()['index'].iloc[::skip].dt.strftime('%Y').values
            # ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
            # ax.xaxis.set_major_locator(mticker.FixedLocator(list(range(df.shape[0]))[::skip]))

            ax.xaxis.set_tick_params(reset=True)

            ticks_pos, ticks_labels = zip(*[(i, j) for i, j in enumerate(df.reset_index()['index'].dt.strftime('%Y')) if int(j) % year_mark == 0])
            ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticks_labels))
            ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_pos))
            ax.set_xlim((0, df.shape[0]))

            # ax.figure.autofmt_xdate()
            ax.grid()
            plt.xticks(rotation=0)

        plt.savefig(f'/tmp/{filename}')
        # shutil.copy(f'/tmp/{filename}', f'/R/Modeling/.trash/nlp_tmp/{filename}')


class LDATopicCompositionRangesView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        corpus_id = args['corpus_id']
        model_id = args['model_id']

        model = get_model(corpus_id, model_id)
        if model is None:
            return {}

        payload = pd.read_json(
            model.get_topic_composition_ranges(
                serialize=True,
            )
        ).to_dict('records')

        return {'topic_ranges': payload}

    def get(self):
        return self.post()


class LDADocsByTopicCompositionView(Resource):
    def post(self):
        args = parse_args(parser_lda)

        corpus_id = args['corpus_id']
        model_id = args['model_id']
        topn = args['topn']
        topic_percentage = args['topic_percentage']
        closest_to_minimum = args['closest_to_minimum']
        topic_percentage = {int(i): j for i, j in topic_percentage.items()}

        model = get_model(corpus_id, model_id)
        if model is None:
            return {}

        return_dict = model.get_docs_by_topic_composition(
            topic_percentage, closest_to_minimum=closest_to_minimum, topn=topn, serialize=True,
        )

        total_found = return_dict['total_found']
        payload = {}

        if total_found > 0:
            payload = pd.read_json(
                return_dict['payload']
            ).to_dict('records')

            for p in payload:
                p['metadata'] = get_document_metadata(p['id'])

        return {'docs': payload, 'total_found': total_found}

    def get(self):
        return self.post()
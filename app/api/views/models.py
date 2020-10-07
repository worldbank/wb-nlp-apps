from flask_restful import Resource, reqparse
import path_manager as pm
import os
import glob


model_map = {
    'AFR': 'Africa',
    'EAP': 'East Asia and Pacific',
    'ECA': 'Europe and Central Asia',

    'LAC': 'Latin America & Caribbean',
    'MENA': 'Middle East and North Africa',
    'RoW': 'Rest Of The World',
    'SAR': 'South Asia',
    'WLD': 'The world Region',
    'M_U': 'None',
    'N.D': 'None',

    'BD': 'Board Documents',
    'CF': 'Country Focus',
    'ESW': 'Economic & Sector Work',
    'PD': 'Project Documents',
    'PR': 'Publications & Research',
    'LIDPL': 'Lending Instrument: DPL',
}


class ModelsList(Resource):
    def post(self):
        models = {}

        for m in glob.iglob(os.path.join(pm.MODELS_DIR, '*')):
            if os.path.isdir(m):
                model = os.path.basename(m)
                models[model] = {}

        for model in models:
            for m in glob.iglob(os.path.join(pm.get_models_path(model), '*')):
                if os.path.isdir(m):

                    corpus_id, model_id = os.path.basename(m).split('-')

                    if model == 'LDA':
                        if not os.path.isfile(os.path.join(m, 'data', f'{corpus_id}_lda_model_{model_id}.mallet.lda')):
                            continue

                    partition_name = '_'.join(model_id.split('_')[:-1])
                    partition_name = model_map.get(partition_name, partition_name)

                    if corpus_id in models[model]:
                        if partition_name in models[model][corpus_id]:
                            models[model][corpus_id][partition_name].append({'model_id': model_id, 'corpus_id': corpus_id})
                        else:
                            models[model][corpus_id][partition_name] = [{'model_id': model_id, 'corpus_id': corpus_id}]
                    else:
                        models[model][corpus_id] = {partition_name: [{'model_id': model_id, 'partition_name': partition_name}]}

        return models

    def get(self):
        return self.post()

"""This script will process and load all configs available into mongodb.
The configs under the cleaning/ directory will be stored in the `cleaning_config` collection
while the configs under the models/ directory will be stored in the `models_config` collection.
"""
import json
from pathlib import Path
from wb_nlp.dir_manager import get_configs_dir
from wb_nlp.interfaces import mongodb
from wb_nlp.utils.scripts import load_config
from wb_nlp.types.cleaning import CleaningConfig
from wb_nlp.types.models import LDAModelConfig, MalletModelConfig, Word2VecModelConfig

from pymongo.errors import DuplicateKeyError

cleaning_configs_collection = mongodb.get_cleaning_configs_collection()

for cfg_path in Path(get_configs_dir('cleaning')).glob('*.yml'):
    config = load_config(cfg_path, 'cleaning_config')
    config = json.loads(CleaningConfig(**config).json())

    config["_id"] = config["cleaning_config_id"]

    try:
        cleaning_configs_collection.insert_one(config)
        print(config)
    except DuplicateKeyError:
        print(f"Config {cfg_path} already in database...")

    print()


model_configs_collection = mongodb.get_model_configs_collection()


model_config_set = [
    (LDAModelConfig, "lda"),
    (MalletModelConfig, "mallet"),
    (Word2VecModelConfig, "word2vec"),
]

for model_config_type, model_name in model_config_set:
    for cfg_path in Path(get_configs_dir('models', model_name)).glob('*.yml'):
        config = load_config(cfg_path, 'model_config')
        config = json.loads(model_config_type(**config).json())

        config["_id"] = config["model_config_id"]

        try:
            model_configs_collection.insert_one(config)
            print(config)
        except DuplicateKeyError:
            print(f"Config {cfg_path} already in database...")

        print()

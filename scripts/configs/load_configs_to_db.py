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
from pymongo.errors import DuplicateKeyError

cleaning_config_collection = mongodb.get_cleaning_config_collection()

for cfg_path in Path(get_configs_dir('cleaning')).glob('*.yml'):
    config = load_config(cfg_path, 'cleaning_config')
    config = json.loads(CleaningConfig(**config).json())

    CFG_PATH = str(cfg_path)

    config["_id"] = config["cleaning_config_id"]

    try:
        cleaning_config_collection.insert_one(config)
        print(config)
    except DuplicateKeyError:
        print(f"Config {cfg_path} already in database...")

    print()

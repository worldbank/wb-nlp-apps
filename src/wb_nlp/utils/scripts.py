from pathlib import Path
import yaml
import hashlib
import json


def load_config(config_path: Path, config_root: str, logger=None) -> dict:
    if logger is not None:
        logger.info(f'Load config file {config_path}...')
    with open(config_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
        config = config[config_root]

    if logger is not None:
        logger.info(config)

    return config


def generate_model_hash(config: dict) -> str:
    return hashlib.md5(json.dumps(config, sort_keys=True).encode('utf-8')).hexdigest()


def load_file(fname: Path, split: bool = True):
    with open(fname) as fl:
        txt = fl.read()

    return txt.split() if split else txt


def generate_files(path: Path, split: bool = True):
    return map(lambda x: load_file(x, split=split), path.glob('*.txt'))


def create_get_directory(parent: Path, child: str) -> Path:
    path = parent / child
    if not path.exists():
        path.mkdir(parents=True)

    return path

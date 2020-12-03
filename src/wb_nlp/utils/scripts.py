'''
Module containing common functions used across the scripts.
'''
from pathlib import Path
import os
import hashlib
import json
import yaml
from dask.distributed import Client, LocalCluster


def load_config(config_path: Path, config_root: str, logger=None) -> dict:
    '''
    Function to load a yaml config file and returns a dictionary version of the config.
    '''
    if logger is not None:
        logger.info(f'Load config file {config_path}...')
    with open(config_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
        config = config[config_root]

    if logger is not None:
        logger.info(config)

    return config


def generate_model_hash(config: dict) -> str:
    '''
    Computes an md5 hash of a config which can be used as a unique identifier.
    '''
    return hashlib.md5(json.dumps(config, sort_keys=True).encode('utf-8')).hexdigest()


def load_file(fname: Path, split: bool = True):
    '''
    Simply loads a file and has an option to return the raw string or a list split by whitespaces.
    '''
    with open(fname) as open_file:
        txt = open_file.read()

    return txt.split() if split else txt


def generate_files(path: Path, split: bool = True):
    '''
    A generator that loads text files given a directory.
    '''
    return map(lambda x: load_file(x, split=split), path.glob('*.txt'))


def create_get_directory(parent: Path, child: str) -> Path:
    '''
    A helper function that automatically creates a directory if it doesn't exist.
    '''
    path = parent / child
    if not path.exists():
        path.mkdir(parents=True)

    return path


def create_dask_cluster(logger=None):
    '''
    This function creates a local dask cluster.
    '''
    if logger:
        logger.info('Creating dask client...')
    cluster = LocalCluster(n_workers=max(1, os.cpu_count() - 4), dashboard_address=':8887',
                           threads_per_worker=1, processes=True, memory_limit=0)
    client = Client(cluster)
    if logger:
        logger.info(client)
        logger.info(client.dashboard_link)

    return client

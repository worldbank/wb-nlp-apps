'''
Module containing common functions used across the scripts.
'''
from pathlib import Path
import logging
import os
import sys
import hashlib
import json
import yaml
import click
from dask.distributed import Client, LocalCluster
# export DASK_DISTRIBUTED__SCHEDULER__ALLOWED_FAILURES=210
# export DASK_DISTRIBUTED__COMM__TIMEOUTS__CONNECT=60
# export DASK_DISTRIBUTED__COMM__RETRY__COUNT=20
from wb_nlp.processing.corpus import load_file, generate_files


@click.command()
@click.option('-c', '--config', 'cfg_path', required=False,
              type=click.Path(exists=False), help='path to yaml config file')
@click.option('--input-file', 'input_file', required=False,
              type=click.Path(exists=False), help='path to wiki articles generated by gensim.scripts.segment_wiki')
@click.option('--output-file', 'output_file', required=False,
              type=click.Path(exists=False), help='path to output json file of article titles and intros')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
def get_command_options(**kwargs):
    '''
    Generic command line arguments extractor.

    Let the individual script handle the extraction, validation, and
    extraction of relevant parameters.

    Returns a dictionary of arguments.
    '''
    return kwargs


def configure_logger(log_level):
    '''
    Configures how the logger output is formatted.
    '''
    logging.basicConfig(stream=sys.stdout,
                        level=log_level,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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


def create_get_directory(parent: Path, child: str) -> Path:
    '''
    A helper function that automatically creates a directory if it doesn't exist.
    '''
    path = parent / child
    if not path.exists():
        path.mkdir(parents=True)

    return path


def create_dask_cluster(logger=None, n_workers=None):
    '''
    This function creates a local dask cluster.
    '''
    if n_workers is not None:
        n_workers = int(n_workers)

    if logger:
        logger.info('Creating dask client...')
    cluster = LocalCluster(n_workers=max(1, os.cpu_count() - 4) if n_workers is None else n_workers, dashboard_address=':8887',
                           threads_per_worker=1, processes=True, memory_limit=0)
    client = Client(cluster)
    if logger:
        logger.info(client)
        logger.info(client.dashboard_link)

    return client

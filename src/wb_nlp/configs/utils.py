from pathlib import Path
import yaml


def load_config(config_path: Path, config_root: str, logger=None) -> dict:
    if logger is not None:
        logger.info(f'Load config file {config_path}...')
    with open(config_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
        config = config[config_root]

    if logger is not None:
        logger.info(config)

    return config

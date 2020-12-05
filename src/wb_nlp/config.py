from wb_nlp.configs.default import default_config


def get_config(config: dict) -> None:
    CONFIG = {}
    CONFIG['cleaner'] = config['cleaner_config']
    CONFIG['spell_checker'] = config['spell_checker_config']
    CONFIG['respeller'] = config['respeller_config']

    return CONFIG

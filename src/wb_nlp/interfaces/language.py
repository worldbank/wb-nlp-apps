import enchant
from wb_nlp import dir_manager

_EN_DICT = None


def get_en_dict():
    global _EN_DICT
    if _EN_DICT is None:
        _EN_DICT = enchant.DictWithPWL('en_US', pwl=dir_manager.get_data_dir(
            "whitelists", "whitelists", "doc-freq-wiki-wordlist.txt"))
    return _EN_DICT

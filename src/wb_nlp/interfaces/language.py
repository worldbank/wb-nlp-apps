import enchant
from wb_nlp import dir_manager


class Language:
    def __init__(self, tag="en_US", pwl=dir_manager.get_data_dir(
            "whitelists", "whitelists", "doc-freq-wiki-wordlist.txt")
    ):
        self.tag = tag
        self.pwl = pwl
        self.init_en_dict()

    def get_en_dict(self):
        # Use this paradigm since enchant.DictWithPWL with pwl raises an error
        # when unpickled.
        if self.en_dict is None:
            self.init_en_dict()

        return self.en_dict

    def init_en_dict(self):
        # self.en_dict = enchant.DictWithPWL(self.tag, pwl=self.pwl)
        self.en_dict = enchant.Dict(self.tag)

        with open(self.pwl) as whitelist_words_file:

            for word in whitelist_words_file.readlines():
                word = word.strip()

                # add word to personal dictionary
                # en_us.add(word)

                # add word just for this session
                self.en_dict.add_to_session(word)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["en_dict"] = None

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.init_en_dict()


EN_LANG = None


def get_en_dict():
    global EN_LANG
    if EN_LANG is None:
        EN_LANG = Language()
    return EN_LANG.get_en_dict()

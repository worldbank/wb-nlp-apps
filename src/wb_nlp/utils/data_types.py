
'''This module is a collection of extended data types.
'''
from wb_nlp.utils.scripts import generate_model_hash


class HashableDict(dict):
    '''This is a wrapper class to make a dictionary hashable.
    '''

    def __hash__(self):
        return hash(generate_model_hash(config=self))

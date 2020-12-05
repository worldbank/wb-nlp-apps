# -*- coding: utf-8 -*-
import os
from wb_nlp.dir_manager import get_data_dir

WHITELIST_PATH = get_data_dir('whitelists', 'extraction')


def get_country_csv():
    return os.path.join(WHITELIST_PATH, 'whitelist_countries_multilingual.csv')

def get_wb_presidents_csv():
    return os.path.join(WHITELIST_PATH, 'wb_presidents.csv')

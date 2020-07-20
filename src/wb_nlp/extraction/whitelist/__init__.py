# -*- coding: utf-8 -*-
import os

WHITELIST_PATH = os.path.dirname(os.path.abspath(__file__))


def get_country_csv():
    return os.path.join(WHITELIST_PATH, 'whitelist_countries_multilingual.csv')

def get_wb_presidents_csv():
    return os.path.join(WHITELIST_PATH, 'wb_presidents.csv')

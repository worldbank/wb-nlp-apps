import pandas as pd
from wb_nlp.extraction import whitelist


def get_countries_mapping():
    country_df = pd.read_csv(whitelist.get_country_csv(), index_col=0, header=None)

    country_mapping = {}
    for country_code, names in country_df.iterrows():
        names = names.dropna().values
        for name in names:
            country_mapping[name] = {'code': country_code, 'normalized': names[0]}

    return country_mapping


def get_wb_presidents_mapping():
    wb_presidents_df = pd.read_csv(whitelist.get_wb_presidents_csv(), index_col=None, header=None)

    wb_presidents_mapping = {}
    for _, names in wb_presidents_df.iterrows():
        names = names.dropna().values
        for name in names:
            wb_presidents_mapping[name] = {'code': '', 'normalized': names[0]}

    return wb_presidents_mapping

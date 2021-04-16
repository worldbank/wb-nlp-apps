import re
from collections import Counter

import pandas as pd
from flashtext import KeywordProcessor

from wb_nlp.extraction.whitelist import mappings
from wb_nlp.dir_manager import get_data_dir
country_code_processor = KeywordProcessor()
country_group_processor = KeywordProcessor()


def get_normalized_country_group_name(code):
    return [
        code,
        code.lower(),
        code.replace("+", " "),
        code.replace("_", " "),
    ]


country_groups_map = pd.read_excel(
    get_data_dir("whitelists", "countries", "codelist.xlsx"),
    sheet_name="groups", header=1, index_col=0).apply(lambda col_ser: col_ser.dropna().index.tolist(), axis=0).to_dict()

country_group_processor.add_keywords_from_dict(
    {k: get_normalized_country_group_name(k) for k in country_groups_map})

mapping = mappings.get_countries_mapping()
country_map = {}
sep = "$"
anchor_code = f"country-code"
for cname, normed in mapping.items():
    # Make sure to add a trailing space at the end of the code below.
    # This guarantees that we isolate the token from symbols, e.g., comma, period, etc.
    code = f"{anchor_code}{sep}{normed['code']} "
    if code in country_map:
        country_map[code].append(cname)
    else:
        country_map[code] = [cname]

country_code_processor.add_keywords_from_dict(country_map)


def replace_country_group_names(txt):
    return country_group_processor.replace_keywords(txt)


def replace_countries(txt):
    return country_code_processor.replace_keywords(txt)


def get_country_counts(txt):
    txt = re.sub(r"\s+", " ", txt)
    try:
        replaced = replace_countries(txt)
    except IndexError:
        return None
    counts = Counter([i.split('$')[-1].strip()
                     for i in replaced.split() if i.startswith(anchor_code)])
    counts = dict(counts.most_common())

    return counts

import re
from collections import Counter
from wb_nlp.extraction.whitelist import mappings

from flashtext import KeywordProcessor
country_code_processor = KeywordProcessor()

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


def replace_countries(txt):
    return country_code_processor.replace_keywords(txt)


def get_country_counts(txt):
    txt = re.sub(r"\s+", " ", txt)
    try:
        replaced = replace_countries(txt)
    except IndexError:
        return None
    return Counter([i.split('$')[-1].strip() for i in replaced.split() if i.startswith(anchor_code)])

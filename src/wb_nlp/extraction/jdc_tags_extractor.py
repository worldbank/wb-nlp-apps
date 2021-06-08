from collections import Counter

import pandas as pd
from flashtext import KeywordProcessor
import inflect
from wb_nlp.dir_manager import get_data_dir

jdc_tags_processor = KeywordProcessor()
inflect_engine = inflect.engine()

# input schema
# -> tag_value
# -> tag_prototypes

# Definition of data input:
# The input to the tag extractor is an excel or csv file.
# The first column of the data must be the intended tag keyword.
# To remove ambiguity, a header with name "tag_keyword" must be present.
# Additionally, all non-empty values in the columns to the right of the tag keyword are considered as prototypes.
# Occurences of these prototypes will be mapped to the tag keyword.


def get_keywords_mapping(tags_sheet):
    tags_mapping = tags_sheet.set_index("tag_keyword").T.apply(
        # If prototypes have "underscores" create a copy with the underscore replaced with a space.
        lambda x: [[i] if "_" not in i else [i, i.replace("_", " ")] for i in x.dropna().tolist()] +

        # Add the tag keyword as well
        [[x.name, x.name.replace("_", " ")]])

    # Clean up the keywords to remove duplicates.
    tags_mapping = tags_mapping.map(
        lambda x: sorted(set([j for i in x for j in i])))

    tags_mapping = tags_mapping.map(
        lambda x: x + [inflect_engine.plural(i) for i in x if "_" not in i])

    # Clean up the keywords to remove duplicates.
    tags_mapping = tags_mapping.map(
        lambda x: sorted(set(x)))

    return tags_mapping


tags_sheet = pd.read_excel(get_data_dir("whitelists", "jdc", "List_filtering_keywords.xlsx"),
                           header=None, index_col=0).rename(columns={1: "tag_keyword"})


tags_mapping = get_keywords_mapping(tags_sheet=tags_sheet)
if "Kakuma (Kenya)" in tags_mapping:
    tags_mapping.pop("Kakuma (Kenya)")


jdc_tags_processor.add_keywords_from_dict(tags_mapping)


def get_jdc_tag_counts(txt):
    data = []

    for tag, value in Counter(jdc_tags_processor.extract_keywords(txt)).most_common():
        data.append(dict(
            tag=tag,
            count=value
        ))

    return data

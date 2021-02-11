from wb_nlp.types import metadata
from collections import Counter
from wb_nlp.interfaces.mongodb import get_metadata_collection

nlp_coll = get_metadata_collection()


def get_invalid_values(field, enum_type, delimiter):
    """
    field: "doc_type"
    enum_type: me.WBDocTypes
    """
    f = nlp_coll.find({field: {"$exists": True}}, projection=[field])
    dc = Counter([i[field] for i in f])

    invalid_values = {}

    for d, c in dc.most_common():

        # Apply this correction for `topics_src` field
        if "Health, Nutrition and Population" in d:
            d = d.replace("Health, Nutrition and Population",
                          "Health; Nutrition and Population")

        if delimiter:
            d_split = d.split(delimiter)
            if len(d_split) == 0:
                d_split = [""]
        else:
            d_split = [d]

        for dd in d_split:
            dd = dd.strip()
            try:
                enum_type(dd)
            except ValueError:
                if dd in invalid_values:
                    invalid_values[dd] += c
                else:
                    invalid_values[dd] = c

    return invalid_values

# from wb_nlp.types import metadata_enums as me
# d = get_invalid_values("topics_src", me.WBTopics, ",")


nlp_coll.find({"path_original": {"$nin": ["", None]}})

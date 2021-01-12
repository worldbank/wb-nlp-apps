from collections import Counter
from wb_nlp.interfaces.mongodb import get_metadata_collection
from wb_nlp.types import metadata_enums as me

nlp_coll = get_metadata_collection()


def get_invalid_values(field, enum_type):
    """
    field: "doc_type"
    enum_type: me.WBDocTypes
    """
    f = nlp_coll.find({field: {"$exists": True}}, projection=[field])
    dc = Counter([i[field] for i in f])

    invalid_values = {}

    for d, c in dc.most_common():
        try:
            enum_type(d)
        except ValueError:
            invalid_values[d] = c

    return invalid_values

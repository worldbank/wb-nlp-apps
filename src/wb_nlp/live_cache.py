from wb_nlp.interfaces import mongodb

docs_metadata_collection = mongodb.get_collection(
    db_name="test_nlp", collection_name="docs_metadata")


DOCS_INT_ID_TO_ID = {r["int_id"]: r["id"]
                     for r in docs_metadata_collection.find({}, projection=["int_id", "id"])}

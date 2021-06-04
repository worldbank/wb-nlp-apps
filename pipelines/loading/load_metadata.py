"""
This script handles the loading of the cleaned metadata into the mongodb.

Further steps:

1. Load data to elasticsearch. Do this by running the following snippet:

    # # # Optional - depends if the index is broken
    # # from elasticsearch_dsl import Index
    # # i = Index(name=elasticsearch.DOC_INDEX, using=elasticsearch.get_client())
    # # i.delete()
    # from wb_nlp.interfaces import elasticsearch, mongodb
    # docs_metadata_coll = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = list(docs_metadata_coll.find({}))
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True, en_txt_only=True, remove_doc_whitespaces=True)
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=False, en_txt_only=True, remove_doc_whitespaces=True)

2. Next clean the documents and generate the vectors for the data.

"""
import json
from pathlib import Path
from wb_nlp import dir_manager
from wb_nlp.interfaces import mongodb


def load_clean_metadata():
    """
    This function loads the cleaned metadata generated from
    pipelines/cleaning/document_pipeline.py to the mongodb database.

    The files are expected to be stored in corpus/<corpus_id>/<l_corpus_id>_clean_metadata.jsonl paths.
    """

    collection = mongodb.get_collection("test_nlp", "docs_metadata")
    ids_in_db = {i["_id"]
                 for i in collection.find({}, projection=["_id"])}

    corpus_path = Path(dir_manager.get_data_dir("corpus"))

    for metadata_file in corpus_path.glob("*/*_clean_metadata.jsonl"):
        corpus_id = metadata_file.parent.name
        print(f"Processing metadata from {corpus_id}...")

        metadata = []

        with open(metadata_file) as open_file:
            for line in open_file:
                line = line.strip()
                meta = json.loads(line)

                if meta["id"] in ids_in_db:
                    continue

                meta["_id"] = meta["id"]

                metadata.append(meta)
                ids_in_db.add(meta["id"])

        print(f"Inserting data for {corpus_id} to DB...")
        collection.insert_many(metadata)


if __name__ == "__main__":
    load_clean_metadata()

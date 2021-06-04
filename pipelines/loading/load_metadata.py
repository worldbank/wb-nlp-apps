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

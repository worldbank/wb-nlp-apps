"""
This script allows the update of all metadata for documents under a given source.
The data/corpus/<corpus_id>/<l_corpus_id>_clean_metadata.jsonl must contain the updated version.

Flow:
1. Get corpus id.
2. Identify ids for which we can update the metadata.
3. Delete

"""
from datetime import datetime
import json
from pathlib import Path
from wb_nlp import dir_manager
from wb_nlp.interfaces import mongodb, elasticsearch


def get_docs_metadata_collection():
    return mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")


def update_metadata_in_mongodb(corpus_id):
    l_corpus_id = corpus_id.lower()

    collection = get_docs_metadata_collection()
    ids_in_db = {i["_id"]
                 for i in collection.find({"corpus": corpus_id}, projection=["_id"])}

    metadata_file = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, f"{l_corpus_id}_clean_metadata.jsonl"))

    if not metadata_file.exists():
        print(f"Metadata file {metadata_file} not found! Exiting...")
        return

    updated_date_published_and_year = []

    print(
        f"Found {len(ids_in_db)} documents found. Loading data from metadata file...")
    with open(metadata_file) as open_file:
        for line in open_file:
            line = line.strip()
            meta = json.loads(line)

            meta["_id"] = meta["id"]

            update_data = dict(
                _id=meta["_id"],
                date_published=meta["date_published"],
                year=meta["year"],
                last_update_date=datetime.now(),
            )

            if meta["_id"] not in ids_in_db:
                update_data.update(meta)

            updated_date_published_and_year.append(update_data)

    print(
        f"Upserting {len(updated_date_published_and_year)} data to mongodb...")
    for upsert_data in updated_date_published_and_year:
        collection.update_one({"_id": upsert_data.pop("_id")}, {
            "$set": upsert_data}, upsert=True)

    print("Finished updating data in mongodb...")


def update_metadata_in_elasticsearch(corpus_id, ignore_existing):
    docs_metadata_coll = get_docs_metadata_collection()
    docs_metadata = list(docs_metadata_coll.find({"corpus": corpus_id}))

    print(
        f"Running elasticsearch data update for {len(docs_metadata)} documents...")
    elasticsearch.make_nlp_docs_from_docs_metadata(
        docs_metadata, ignore_existing=ignore_existing, en_txt_only=True, remove_doc_whitespaces=True)

    print("Finished updating data in elasticsearch...")


def main(corpus_id):
    print(f"Processing data for {corpus_id}...")

    print("update_metadata_in_mongodb")
    update_metadata_in_mongodb(corpus_id)

    print("update_metadata_in_elasticsearch")
    update_metadata_in_elasticsearch(corpus_id, ignore_existing=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--corpus-id', dest='corpus_id',
                        type=str, default="ADB")
    args = parser.parse_args()

    main(**vars(args))

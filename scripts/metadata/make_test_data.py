"""This scripts generates a dummy data set to test the end-to-end implementation of the
metadata preparation, document management, cleaning, model training, and API development.
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from wb_nlp.dir_manager import get_data_dir
from wb_nlp.interfaces import mongodb
from wb_nlp.types import metadata


test_docs_metadata = mongodb.get_collection(
    db_name="test_nlp", collection_name="docs_metadata")

docs_metadata = mongodb.get_docs_metadata_collection()

sample_doc_path = Path(get_data_dir("raw", "sample_data", "TXT_ORIG"))
corpus_path = Path(get_data_dir("corpus"))

for doc_path in sample_doc_path.glob("*.txt"):

    doc_id = doc_path.name.split(".")[0]
    data = docs_metadata.find_one({"id": doc_id})

    if data:
        print(f"{doc_path} is in docs_metadata collection...")
        doc_corpus_path = corpus_path / data["corpus"] / doc_path.name

        if not doc_corpus_path.parent.exists():
            doc_corpus_path.parent.mkdir(parents=True)

        shutil.copy2(doc_path, doc_corpus_path)

        DOC_CORPUS_PATH = str(doc_corpus_path)

        data["path_original"] = DOC_CORPUS_PATH[DOC_CORPUS_PATH.index(
            "/data"):]

        data["_id"] = data["id"]
        data["last_update_date"] = datetime.now()
        data["path_clean"] = None

        # Make sure the data conforms with the expected schema.
        data = json.loads(metadata.MetadataModel(**data).json())

        test_docs_metadata.insert(data)

import json
import pymongo
from wb_nlp.dir_manager import get_data_dir
from wb_nlp.interfaces import mongodb

collection = mongodb.get_metadata_collection()

# client = pymongo.MongoClient(host='mongodb', port=27017)
# db = client['nlp']
# collection = db['metadata']

# Dump file can be generated by running:
# mongoexport --collection=metadata --db=nlp --out=<outfilename>.json
DUMP_FILE = get_data_dir('raw', 'nlp-metadata-wbes2474-20201007.json')

print(f"Start loading data dump {DUMP_FILE} to collection: {collection}")

dump_data = [json.loads(line) for line in open(DUMP_FILE, 'r')]

if isinstance(dump_data, list):
    collection.insert_many(dump_data)
else:
    collection.insert_one(dump_data)

print(f"Finished loading data dump to collection: {collection}")

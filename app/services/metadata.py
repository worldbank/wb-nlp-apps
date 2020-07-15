import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)  # (host='w1lxbdatad07', port=27018)
db = client['nlp']
collection = db['metadata']


def get_documents_metadata(ids, fields=None):
	return [get_document_metadata(id, fields) for id in ids]


def get_document_metadata(id, fields=None):
	return collection.find_one({'_id': id})

def get_data_iterator(filter, projection):
	return collection.find(filter=filter, projection=projection)

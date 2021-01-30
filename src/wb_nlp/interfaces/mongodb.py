import json
import pymongo
from wb_nlp.dir_manager import get_data_dir

MONGODB_CLIENT = None
HOST = "mongodb"
PORT = 27017


def test_or_get_client(host, port):
    # Create a temporary client with short timeout to test for existence.
    _client = pymongo.MongoClient(
        host=host, port=PORT, serverSelectionTimeoutMS=50)

    client = None
    try:
        _client.server_info()

        # Create a new client with now a longer timeout
        client = pymongo.MongoClient(host=host, port=port)

    finally:
        _client.close()

    return client


def get_mongodb_client(host=None, port=None):
    global MONGODB_CLIENT

    _HOST = host or HOST
    _PORT = port or PORT

    if MONGODB_CLIENT is None:
        MONGODB_CLIENT = test_or_get_client(host=_HOST, port=_PORT)
    else:
        try:
            MONGODB_CLIENT.server_info()
        except:
            MONGODB_CLIENT = test_or_get_client(host=_HOST, port=_PORT)

    if MONGODB_CLIENT is None:
        raise ValueError(
            f"Connection is not available due to a possible invalid server details provided. Please confirm host=`{HOST}` and port=`{PORT}` are correct.")

    return MONGODB_CLIENT


def get_collection(db_name, collection_name, host=None, port=None):
    """This is a generic function to get an interface to a given collection.
    """
    client = get_mongodb_client(host, port)
    db = client[db_name]
    collection = db[collection_name]

    return collection


def get_metadata_collection(host=None, port=None):
    return get_collection(host=host, port=port, db_name="nlp", collection_name="metadata")


def get_docs_metadata_collection(host=None, port=None):
    return get_collection(host=host, port=port, db_name="nlp", collection_name="docs_metadata")


def get_cleaning_config_collection(host=None, port=None):
    return get_collection(host=host, port=port, db_name="nlp", collection_name="cleaning_config")


def get_models_config_collection(host=None, port=None):
    return get_collection(host=host, port=port, db_name="nlp", collection_name="models_config")

'''This module is an interface to Milvus.
'''
from milvus import Milvus, DataType

MILVUS_CLIENT = None


def get_milvus_client():
    '''This returns a Milvus client for interfacing with the Milvus server.
    '''
    global MILVUS_CLIENT

    HOST = 'milvus'
    PORT = '19530'

    if MILVUS_CLIENT is None:
        MILVUS_CLIENT = Milvus(HOST, PORT)
    else:
        try:
            MILVUS_CLIENT.server_status()
        except:
            MILVUS_CLIENT = Milvus(HOST, PORT)

    return MILVUS_CLIENT


def get_hex_id(int_id: int):
    return '{:x}'.format(int_id)


def get_int_id(hex_id: str):
    assert len(hex_id) == 15

    return int(hex_id, 16)


def get_collection_ids(collection_name, partition_tag=None):
    '''Get all ids present in the collection. This is useful to check which ids exist to prevent duplicated items.
    https://github.com/milvus-io/milvus/issues/2393#issuecomment-633236922
    '''
    client = get_milvus_client()

    collection_info = client.get_collection_stats(
        collection_name=collection_name)
    partition_list = collection_info["partitions"]
    collection_ids = []

    for partition in partition_list:
        if partition_tag and partition_tag != partition['tag']:
            continue

        segment_list = partition.get("segments")

        if segment_list is None:
            continue

        for segment in segment_list:
            segment_id = segment["id"]

            id_list = client.list_id_in_segment(
                collection_name=collection_name, segment_id=segment_id)

            collection_ids.extend(id_list)

    return collection_ids


def get_embedding_dsl(query_vec, topk, vector_field_name, metric_type="IP"):
    """This method creates a dsl query for the given query vector.
    The distance metric is specified by the `metric_type` parameter.
    """

    dsl = {
        "bool": {
            "must": [
                {
                    "vector": {
                        vector_field_name: {
                            "topk": topk,
                            "query": [query_vec.flatten()],
                            "metric_type": metric_type
                        }
                    }
                }
            ]
        }
    }

    return dsl

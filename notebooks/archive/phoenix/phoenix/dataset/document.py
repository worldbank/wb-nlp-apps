from pymongo import MongoClient
import pandas as pd
import json
import os


class DocumentDB:
    _client = None
    _db = None
    host = os.environ.get('WB_NLP_MONGODB_HOSTNAME', 'localhost')
    port = int(os.environ.get('WB_NLP_MONGODB_PORT', 27017))

    def __init__(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

        self._client = self.get_client()

    def __del__(self):
        try:
            self.close_conn()
        except:
            pass

    def close_conn(self):
        if self._client is not None:
            self._client.close()

    def get_client(self):
        if self._client is None:
            self._client = MongoClient(host=self.host, port=self.port)

        return self._client

    def get_db(self):
        if self._db is None:
            self._db = self._client.wb_nlp_db

        return self._db

    def get_clean_docs_collection(self):
        db = self.get_db()
        return db.clean_docs

    def get_metadata_collection(self):
        db = self.get_db()
        return db.metadata

    def store_data(self, df, coll):
        available_ids = [i['_id'] for i in coll.find(filter={}, projection=['_id'])]

        to_insert_df = df[~df._id.isin(available_ids)]

        inserted = []
        if not to_insert_df.empty:
            datetime_cols = df.columns[df.dtypes == 'datetime64[ns]']

            for col in datetime_cols:
                df[col] = df[col].map(lambda x: x.isoformat() if x else x)

            inserted = coll.insert_many(to_insert_df.to_dict('records'))
            inserted = inserted.inserted_ids

        return {
            'total_docs': coll.count_documents(filter={}),
            'inserted_count': len(inserted),
            'to_insert_count': to_insert_df.shape[0]
        }

    def store_clean_docs_data(self, clean_docs_df):
        clean_docs_coll = self.get_clean_docs_collection()

        assert('_id' in clean_docs_df.columns)
        return self.store_data(clean_docs_df, clean_docs_coll)

    def store_metadata_data(self, metadata_df):
        metadata_coll = self.get_metadata_collection()

        assert('_id' in metadata_df.columns)
        return self.store_data(metadata_df, metadata_coll)

    def find(self, collection, filter, projection=None):
        if projection is None:
            projection = []

        return collection.find(filter=filter, projection=projection)

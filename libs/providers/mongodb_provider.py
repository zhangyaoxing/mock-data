from libs.providers.output_provider import OutputProvider
from pymongo import MongoClient

class MongoDBProvider(OutputProvider):
    def __init__(self, config):
        super().__init__(config)
        self._client = None
        self._db = None
        self._collection = None
        self._connect_to_mongodb()
        self._batch_size = config.get('batch_size', 1)
        self._docs = []
        self._logger.debug(f"Initialized MongoDBProvider with config: {config}")

    def _connect_to_mongodb(self):
        uri = self._config.get('uri', 'mongodb://localhost:27017/test')

        self._client = MongoClient(uri)
        self._db = self._client.get_default_database()
        self._logger.debug(f"Connected to MongoDB at {uri}")

    def _insert(self, docs):
        if self._collection is None:
            self._collection = self._db[self._name]
        self._collection.insert_many(docs)
        self._logger.debug(f"Inserted {len(docs)} documents into collection {self._name}")
    def write(self, data):
        self._docs.append(data)
        if len(self._docs) >= self._batch_size:
            self._insert(self._docs)
            self._docs = []

    def close(self):
        if self._client:
            if len(self._docs) > 0:
                self._insert(self._docs)
            self._client.close()
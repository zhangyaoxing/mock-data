"""MongoDB output provider."""

from typing import Optional, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from mockdata.providers.base import OutputProvider


class MongoDBProvider(OutputProvider):
    """Provider for writing mock data to MongoDB."""

    def __init__(self, config: dict):
        """Initialize MongoDB provider.

        Args:
            config: Configuration with 'uri' and optional 'batch_size'.
        """
        super().__init__(config)
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._collection: Optional[Collection] = None
        self._batch_size = config.get('batch_size', 1000)
        self._docs: List[dict] = []
        self._connect_to_mongodb()
        self._logger.debug(f"Initialized MongoDBProvider with config: {config}")

    def _connect_to_mongodb(self) -> None:
        """Establish connection to MongoDB."""
        uri = self._config.get('uri', 'mongodb://localhost:27017/test')
        self._client = MongoClient(uri)
        self._db = self._client.get_default_database()
        self._logger.debug(f"Connected to MongoDB at {uri}")

    def _insert(self, docs: List[dict]) -> None:
        """Insert documents into MongoDB.

        Args:
            docs: List of documents to insert.
        """
        if self._collection is None:
            self._collection = self._db[self._name]
        
        self._collection.insert_many(docs)
        self._logger.debug(f"Inserted {len(docs)} documents into collection {self._name}")

    def write(self, data: dict) -> None:
        """Buffer data and write in batches to MongoDB.

        Args:
            data: Dictionary to write to MongoDB.
        """
        self._docs.append(data)
        if len(self._docs) >= self._batch_size:
            self._insert(self._docs)
            self._docs = []

    def close(self) -> None:
        """Flush remaining documents and close connection."""
        if self._client:
            if self._docs:
                self._insert(self._docs)
            self._client.close()
            self._logger.debug("Closed MongoDB connection")

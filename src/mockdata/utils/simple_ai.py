"""Guess generator methods based on field names and bson types using a simple AI approach."""

import shutil
from logging import getLogger
from pathlib import Path

import chromadb
from faker import Faker

from mockdata.core.fake_providers import ObjectIdProvider

DBPATH: str = str(Path.home() / ".mock_data/chromadb")
COLLECTION_NAME: str = "methods"


class SimpleAI:
    """Implementation of a simple AI that can guess generator methods
    based on field names and bson types."""

    EXCLUDE_LIST = ["add_provider", "get_providers", "seed", "seed_instance", "items", "keys"]
    # Key: Python type name,
    # Value: List of BSON types that this Python type can be converted to.
    BSON_PY_TYPE_MAPPING = {
        "ZoneInfo": ["string"],
        "bool": ["bool", "string"],
        "Decimal": ["double", "decimal", "string"],
        "date": ["date", "string"],
        "generator": ["generator", "string"],
        "str": ["string"],
        "float": ["double", "decimal", "string"],
        "bytes": ["binData", "string"],
        "int": ["int", "long", "decimal", "string"],
        "time": ["date", "string"],
        "ObjectId": ["objectId", "string"],
        "datetime": ["date", "string"],
    }
    client = chromadb.PersistentClient(path=DBPATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    def __init__(self):
        self.logger = getLogger(self.__class__.__name__)
        if not SimpleAI.collection.count():
            # First time running the program, we need to populate the ChromaDB collection with Faker methods.
            SimpleAI.add_methods()

    @staticmethod
    def refresh_methods():
        """Refresh the ChromaDB collection with Faker methods. Use this if you have updated Faker or added custom providers."""
        SimpleAI.client.delete_collection(name=COLLECTION_NAME)
        SimpleAI.collection = SimpleAI.client.get_or_create_collection(name=COLLECTION_NAME)
        SimpleAI.add_methods()

    @staticmethod
    def add_methods():
        """Add Faker methods to the ChromaDB collection."""
        logger = getLogger(SimpleAI.__name__)
        logger.info("Inspecting Faker methods to initialize...")
        fake = Faker()
        fake.add_provider(ObjectIdProvider)
        methods = dir(fake)
        ids = []
        docs = []
        metadatas = []

        for m in methods:
            if m.startswith("_") or m in SimpleAI.EXCLUDE_LIST:
                continue

            # Get generated value type for each method
            attr = getattr(fake, m)
            if callable(attr):
                try:
                    result = attr()
                    res_type = type(result).__name__
                    bson_types = SimpleAI.BSON_PY_TYPE_MAPPING.get(res_type, ["string"])
                    ids.append(m)
                    # Some method names start with 'py' to indicate they are Python-specific,
                    # we will remove this prefix when adding to the collection.
                    # This achieves a better match with field names that don't have this prefix.
                    docs.append(m if not m.startswith("py") else m[2:])
                    metadatas.append({"bson_types": bson_types})
                    logger.debug(
                        "Added generator method '%s' with result type '%s' for bson types %s",
                        m,
                        res_type,
                        bson_types,
                    )
                except (TypeError, AttributeError):
                    continue
        SimpleAI.collection.add(ids=ids, documents=docs, metadatas=metadatas)  # type: ignore[arg-type]
        logger.info("Added %d methods to ChromaDB collection.", len(ids))

    def guess(self, field_name: str, bson_type: str) -> str:
        """Guess the generator method based on field name and bson type."""
        # If the return type of a method cannot be converted to the bson type,
        # we will not consider this method as a candidate.
        result = SimpleAI.collection.query(
            query_texts=[field_name],
            n_results=1,
            where={"bson_types": {"$contains": bson_type}},  # type: ignore
            include=[],
        )
        gen_method = result["ids"][0][0]
        return gen_method

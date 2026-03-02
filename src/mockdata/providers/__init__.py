"""Output providers for writing mock data to various destinations."""

from mockdata.providers.base_provider import OutputProvider
from mockdata.providers.ejson_provider import EJsonProvider
from mockdata.providers.kafka_provider import KafkaProvider
from mockdata.providers.mongodb_provider import MongoDBProvider

__all__ = ["OutputProvider", "EJsonProvider", "MongoDBProvider", "KafkaProvider"]

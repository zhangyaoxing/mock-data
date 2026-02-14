"""Output providers for writing mock data to various destinations."""

from mockdata.providers.base import OutputProvider
from mockdata.providers.ejson import EJsonProvider
from mockdata.providers.mongodb import MongoDBProvider
from mockdata.providers.kafka import KafkaProvider

__all__ = ["OutputProvider", "EJsonProvider", "MongoDBProvider", "KafkaProvider"]

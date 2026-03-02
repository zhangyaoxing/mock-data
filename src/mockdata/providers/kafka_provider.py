"""Kafka output provider."""

from bson import json_util
from kafka import KafkaProducer

from mockdata.providers.base_provider import OutputProvider


class KafkaProvider(OutputProvider):
    """Provider for writing mock data to Kafka topics."""

    def __init__(self, config: dict):
        """Initialize Kafka provider.

        Args:
            config: Configuration with 'bootstrap_servers'.
        """
        super().__init__(config)
        self._producer = KafkaProducer(
            bootstrap_servers=config.get("bootstrap_servers", "localhost:9092"),
            value_serializer=lambda v: json_util.dumps(v).encode("utf-8"),
        )
        self._logger.debug("Initialized KafkaProvider with config: %s", config)

    def write(self, data: dict) -> None:
        """Write data to Kafka topic.

        Args:
            data: Dictionary to send as message to Kafka topic.
        """
        self._producer.send(self._name, value=data)
        self._producer.flush()
        self._logger.debug("Data sent to Kafka topic %s", self._name)

    def close(self) -> None:
        """Close the Kafka producer connection."""
        if self._producer:
            self._producer.close()
            self._logger.debug("Closed Kafka producer")

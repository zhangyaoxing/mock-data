import json
from libs.providers.output_provider import OutputProvider
from kafka import KafkaProducer
from bson import json_util

class KafkaProvider(OutputProvider):
    def __init__(self, config):
        super().__init__(config)
        self._producer = KafkaProducer(
            bootstrap_servers=config.get("bootstrap_servers", "localhost:9092"),
            value_serializer=lambda v: json_util.dumps(v).encode('utf-8')
        )

    def write(self, data):
        """
        Write the mocked data to the Kafka topic.
        The topic is set in the schema configuration (The `name` field).
        """
        self._producer.send(self._name, value=data)
        self._producer.flush()
        self._logger.debug(f"Data sent to Kafka topic {self._name}.")
    
    def close(self):
        """
        Close the Kafka producer connection.
        """
        self._producer.close()
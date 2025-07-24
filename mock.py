# mock.py
import sys
from libs.mock_data import MockData
from libs.providers.ejson_provider import EJsonProvider
from libs.providers.mongodb_provider import MongoDBProvider
from libs.providers.kafka_provider import KafkaProvider
from libs.utils import *
from bson import json_util
import os
import json


logger = get_logger(__name__)

def read_schemas():
    """
    Read all JSON schema files from the schemas directory.
    Returns a dictionary with filenames as keys and file contents as values.
    """
    logger.info(cyan("Reading schemas definition files from the schemas directory."))
    schemas = {}
    schemas_path = get_script_path("schemas")
    
    for filename in os.listdir(schemas_path):
        if filename.endswith(".json"):
            file_path = os.path.join(schemas_path, filename)
            logger.info(f"Loading: {cyan(filename)}")
            with open(file_path, 'r') as file:
                schemas[filename] = json.load(file)
    logger.info(bold(green("All schemas loaded successfully.")))
    return schemas

def add_providers(mock_data):
    """
    Add output providers to the MockData instance based on the configuration.
    """
    config = load_config()
    output_provider_config = config.get("output", {})
    if "ejson" in output_provider_config:
        mock_data.add_provider(EJsonProvider(output_provider_config["ejson"]))
    if "mongodb" in output_provider_config:
        mock_data.add_provider(MongoDBProvider(output_provider_config["mongodb"]))
    if "kafka" in output_provider_config:
        mock_data.add_provider(KafkaProvider(output_provider_config["kafka"]))

spinner = ['|', '/', '-', '\\']
if __name__ == "__main__":
    config = load_config()
    schemas = read_schemas()
    logger.info(cyan("Mocking data based on the provided schemas."))
    for name, schema in schemas.items():
        schema["name"] = name if "name" not in schema else schema["name"]
        mock_data = MockData(schema)
        add_providers(mock_data)
        objects = mock_data.run()
        processed_count = 0
        for obj in objects:
            processed_count += 1
            sys.stdout.write(f"\r{spinner[processed_count % len(spinner)]} {round(processed_count / mock_data._count * 100, 2)}%")
            sys.stdout.flush()
        mock_data.close()
        sys.stdout.write("\r")
        sys.stdout.flush()
        logger.info(bold(green(f"Successfully mocked {processed_count} objects for schema: {schema['name']}")))
# mock.py
import sys
from libs.mock_data import MockData
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

spinner = ['|', '/', '-', '\\']
if __name__ == "__main__":
    schemas = read_schemas()
    logger.info(cyan("Mocking data based on the provided schemas."))
    for name, schema in schemas.items():
        mock_data = MockData(schema)
        objects = mock_data.mock()
        processed_count = 0
        for obj in objects:
            logger.debug(f"Generated object for schema {name}: {json_util.dumps(obj, indent=2)}")
            # TODO: Save or process the generated object as needed
            processed_count += 1
            sys.stdout.write(f"\r{spinner[processed_count % len(spinner)]} {processed_count}/{mock_data._count}")
            sys.stdout.flush()
# mock.py
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

if __name__ == "__main__":
    schemas = read_schemas()
    logger.info(cyan("Mocking data based on the provided schemas."))
    for name, schema in schemas.items():
        obj = MockData(schema).mock()
        print(json_util.dumps(obj, indent=2))
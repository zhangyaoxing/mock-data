from libs.providers.output_provider import OutputProvider
from libs.utils import get_script_path
from bson import json_util

class EJsonProvider(OutputProvider):
    def __init__(self, config):
        super().__init__(config)
        self._file = None
        self._logger.debug(f"Initialized EJsonProvider with config: {config}")

    def write(self, data):
        if not self._file:
            full_path = get_script_path(f"{self._config.get('folder', 'output')}/{self._name}.ejson")
            self._file = open(full_path, 'w')
            self._logger.debug(f"Opened EJSON file for writing: {full_path}")
        # Write data to the file in EJSON format
        ejson_data = json_util.dumps(data)
        self._file.write(ejson_data)
        self._file.write('\n')
    
    def close(self):
        # Close the file after writing
        self._file.close()
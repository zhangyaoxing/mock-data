from libs.providers.output_provider import OutputProvider
from libs.utils import get_script_path
from bson import json_util

class EJsonProvider(OutputProvider):
    def __init__(self, config):
        super().__init__(config)
        self._file = None

    def write(self, data):
        if not self._file:
            full_path = get_script_path(f"{self._config.get('folder', 'output')}/{self._name}.ejson")
            self._file = open(full_path, 'w')
        # Write data to the file in EJSON format
        ejson_data = json_util.dumps(data)
        self._file.write(ejson_data)
        self._file.write('\n')
    
    def close(self):
        # Close the file after writing
        self._file.close()
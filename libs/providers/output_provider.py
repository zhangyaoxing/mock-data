from abc import abstractmethod
from libs.utils import get_logger
class OutputProvider:
    def __init__(self, config):
        self._config = config
        self._logger = get_logger(__name__)

    @abstractmethod
    def write(self):
        pass
    
    @abstractmethod
    def close(self):
        """
        Close any resources if necessary.
        """
        pass

    def set_name(self, name):
        """
        Set the name for the output file.
        """
        self._name = name
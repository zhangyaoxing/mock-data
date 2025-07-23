from abc import abstractmethod

class OutputProvider:
    def __init__(self, config):
        self._config = config
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
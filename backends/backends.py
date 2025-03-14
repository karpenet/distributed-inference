from abc import ABC, abstractmethod

class BaseBackend(ABC):
    @abstractmethod
    def pack_model(self, model):
        pass

    @abstractmethod
    def export_model(self, model, path):
        pass

    @abstractmethod
    def unpack_model(self, packed_model):
        pass



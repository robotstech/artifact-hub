from abc import ABC, abstractmethod


class BaseBackend(ABC):
    @abstractmethod
    def pull_into(self, destination_path: str, version_id: str):
        pass

    @abstractmethod
    def push(self, source_path: str, title: str, description: str):
        pass

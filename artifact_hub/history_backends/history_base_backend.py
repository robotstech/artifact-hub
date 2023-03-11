from abc import ABC, abstractmethod


class HistoryBaseBackend(ABC):
    @abstractmethod
    def get_latest_version_id(self) -> int:
        pass

    @abstractmethod
    def add_new_version(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

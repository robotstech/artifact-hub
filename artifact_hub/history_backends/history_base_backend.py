import secrets
from abc import ABC, abstractmethod


class HistoryBaseBackend(ABC):
    @abstractmethod
    def get_latest_version_id(self) -> str:
        pass

    @abstractmethod
    def add_new_version(self) -> str:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @staticmethod
    def generate_new_version_id() -> str:
        return secrets.token_hex(16)

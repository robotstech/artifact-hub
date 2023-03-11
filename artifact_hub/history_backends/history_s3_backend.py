import json
import urllib.request

import boto3
from botocore.exceptions import ClientError

from artifact_hub.history_backends.history_base_backend import HistoryBaseBackend


class HistoryS3Backend(HistoryBaseBackend):
    HISTORY = "history"
    HISTORY_PATH = "res/history"

    def __init__(self, bucket: str, folder: str, object_id):
        self.__repo_path = f"{folder}/{object_id}"
        self.__store = boto3.resource('s3').Bucket(bucket)
        self.__history = self.__load_history()

    def __load_history(self):
        try:
            self.__store.download_file(f"{self.__repo_path}/{self.HISTORY}", self.HISTORY_PATH)
            with open(self.HISTORY_PATH) as file:
                self.__history = list(map(lambda x: x.split(), file))

            return list(map(
                lambda y: (int(y[0]), y[1]),
                self.__history
            ))

        except ClientError:
            return []

    def sync(self):
        with open(self.HISTORY_PATH, 'w') as file:
            file.writelines(map(lambda x: f"{x[0]} {x[1]}\n", self.__history))
        self.__store.upload_file(self.HISTORY_PATH, f"{self.__repo_path}/{self.HISTORY}")

    def add_new_version(self):
        self.__history.append((self.get_next_version_id(), self.__get_current_datetime_string()))
        return self.get_latest_version_id()

    def revert_latest_version(self):
        self.__history.pop()

    @staticmethod
    def __get_current_datetime_string():
        return json.loads(
            urllib.request.urlopen(
                "https://www.timeapi.io/api/Time/current/zone?timeZone=UTC"
            ).read().decode()
        )["dateTime"]

    def get_latest_version_id(self) -> int:
        return self.__history[-1][0]

    def get_next_version_id(self) -> int:
        return self.get_latest_version_id() + 1

    def is_empty(self) -> bool:
        return len(self.__history) == 0

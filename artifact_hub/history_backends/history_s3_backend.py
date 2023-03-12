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

    @property
    def history(self):
        try:
            self.__store.download_file(f"{self.__repo_path}/{self.HISTORY}", self.HISTORY_PATH)
            with open(self.HISTORY_PATH) as file:
                history = list(map(lambda x: x.split(), file))

            return history

        except ClientError:
            return []

    def __sync(self, history):
        with open(self.HISTORY_PATH, 'w') as file:
            file.writelines(map(lambda x: f"{x[0]} {x[1]}\n", history))
        self.__store.upload_file(self.HISTORY_PATH, f"{self.__repo_path}/{self.HISTORY}")

    def add_new_version(self):
        history = self.history
        next_version_id = self.generate_new_version_id()
        history.append((next_version_id, self.__get_current_datetime_string()))
        self.__sync(history.copy())
        return next_version_id

    @staticmethod
    def __get_current_datetime_string():
        return json.loads(
            urllib.request.urlopen(
                "https://www.timeapi.io/api/Time/current/zone?timeZone=UTC"
            ).read().decode()
        )["dateTime"]

    def get_latest_version_id(self) -> str:
        return self.history[-1][0]

    def is_empty(self) -> bool:
        return len(self.history) == 0

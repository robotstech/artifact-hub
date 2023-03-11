import logging
import os

import boto3

from artifact_hub.backends.base_backend import BaseBackend
from artifact_hub.history_backends.history_base_backend import HistoryBaseBackend

logger = logging.getLogger("artifact_hub")


class S3Backend(BaseBackend):
    TITLE = "title"
    TITLE_PATH = "res/title"
    DESCRIPTION = "description"
    DESCRIPTION_PATH = "res/description"
    INIT = "init"
    INIT_PATH = "res/init"

    def __init__(self, bucket: str, folder: str, repo_id: str, history_backend: HistoryBaseBackend):
        self.__store = boto3.resource('s3').Bucket(bucket)
        self.__folder = folder
        self.__repo_id = repo_id
        self.__repo_base_path = f"{self.__folder}/{self.__repo_id}"
        self.__history = history_backend

        # check if repo init existed
        if self.__history.is_empty():
            logger.info(f"{repo_id} not found, creating now ...")
            self.__create_text_file(self.INIT_PATH, self.INIT)

            # create one if init does not exist
            self.push(
                self.INIT_PATH, f"{self.__repo_id}'s {self.INIT}",
                f"initializing {self.__repo_id} in the hub"
            )

            # feedback that repo is loaded
        logger.info(f"{repo_id} loaded")

    def __get_repo_version_path(self, version_id):
        return f"{self.__repo_base_path}/{version_id}"

    def __get_repo_path(self, version_id):
        return f"{self.__get_repo_version_path(version_id)}/{self.__repo_id}"

    def __get_repo_object_path(self, version_id, *args):
        return os.path.normpath(os.path.join(self.__get_repo_path(version_id), os.path.join(*args)))

    def __get_repo_version_description_path(self, version_id):
        return f"{self.__get_repo_version_path(version_id)}/{self.DESCRIPTION}"

    def __get_repo_version_title_path(self, version_id):
        return f"{self.__get_repo_version_path(version_id)}/{self.TITLE}"

    @staticmethod
    def __create_text_file(filepath: str, content: str):
        with open(filepath, 'w') as file:
            file.write(content)
        return filepath

    def pull_into(self, destination_path: str, version_id: int = None):
        if not version_id:
            version_id = self.__history.get_latest_version_id()

        repo_version_path = self.__get_repo_version_path(version_id)
        for obj in self.__store.objects.filter(Prefix=self.__get_repo_path(version_id)):
            obj_key_dest_path = os.path.normpath(os.path.join(destination_path, obj.key)) \
                .replace(repo_version_path, "", 1)

            if not os.path.exists(os.path.dirname(obj_key_dest_path)):
                os.makedirs(os.path.dirname(obj_key_dest_path))
            self.__store.download_file(obj.key, obj_key_dest_path)

    def push(self, source_path: str, title: str, description: str):
        try:
            version_id = self.__history.add_new_version()

            self.__store.upload_file(
                self.__create_text_file(self.TITLE_PATH, title),
                self.__get_repo_version_title_path(version_id)
            )

            self.__store.upload_file(
                self.__create_text_file(self.DESCRIPTION_PATH, description),
                self.__get_repo_version_description_path(version_id)
            )

            if os.path.isdir(source_path):
                for path, sub_dirs, files in os.walk(source_path):
                    for file in files:
                        dest_path = path.replace(source_path, "")
                        __s3file = self.__get_repo_object_path(version_id, dest_path, file)
                        __local_file = os.path.join(path, file)
                        self.__store.upload_file(__local_file, __s3file)
            else:
                self.__store.upload_file(
                    source_path,
                    self.__get_repo_object_path(version_id, os.path.basename(source_path))
                )

            return self.__history.get_latest_version_id()

        except Exception as e:
            logger.warning(f"could not push: {e}")

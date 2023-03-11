import os.path
import secrets

import boto3

from artifact_hub import s3_hub
from artifact_hub.backends.s3_backend import S3Backend
from artifact_hub.history_backends.history_s3_backend import HistoryS3Backend


def test_hub_initialization_s3_hub():
    folder = "folder"
    object_id = "object_id"
    bucket_name = "iamr0b0tx-development"

    hub = s3_hub(bucket_name, folder, object_id)
    assert isinstance(hub, S3Backend)

    # download history file
    boto3.resource('s3').Bucket(bucket_name).download_file(f"{folder}/{object_id}/{HistoryS3Backend.HISTORY}",
                                                           HistoryS3Backend.HISTORY_PATH)
    with open(HistoryS3Backend.HISTORY_PATH) as file:
        assert file.read().startswith("0 ")

    random_idx = secrets.token_hex(3)
    sample_file_path = "res/sample_file.txt"
    lines = [f"{random_idx}: this is a sample file\n", "its has three lines\n", "This is the third line\n"]
    with open(sample_file_path, 'w') as file:
        file.writelines(lines)

    latest_version_id = hub.push(sample_file_path, "pushing sample file", "this is a test for sample file")
    assert latest_version_id is not None

    # create temp dir
    if not os.path.exists("temp"):
        os.mkdir("temp")

    hub.pull_into("temp")
    with open(f"temp/{object_id}/{os.path.basename(sample_file_path)}") as file:
        assert file.readlines() == lines

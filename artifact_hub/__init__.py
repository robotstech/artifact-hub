import os

from artifact_hub.backends.s3_backend import S3Backend
from artifact_hub.history_backends.history_s3_backend import HistoryS3Backend

if not os.path.exists("res"):
    os.mkdir("res")


def s3_hub(bucket, folder, object_id):
    history = HistoryS3Backend(bucket, folder, object_id)
    backend = S3Backend(bucket, folder, object_id, history)
    return backend

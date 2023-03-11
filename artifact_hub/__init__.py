from artifact_hub.backends.s3_backend import S3Backend
from artifact_hub.history_backends.history_s3_backend import HistoryS3Backend

VERSION = '0.0.1'


def s3_hub(bucket, folder, object_id):
    history = HistoryS3Backend(bucket, folder, object_id)
    backend = S3Backend(bucket, folder, object_id, history)
    return backend

import os.path
import secrets

from artifact_hub import s3_hub
from artifact_hub.backends.s3_backend import S3Backend


def test_hub_initialization_s3_hub():
    folder = "folder"
    object_id = f"object_{secrets.token_hex(3)}"
    bucket_name = "iamr0b0tx-development"

    hub = s3_hub(bucket_name, folder, object_id)
    assert isinstance(hub, S3Backend)

    random_idx = secrets.token_hex(3)
    sample_file_path = "res/sample_file.txt"
    lines = [f"{random_idx}: this is a sample file\n", "its has three lines\n", "This is the third line\n"]
    with open(sample_file_path, 'w') as file:
        file.writelines(lines)

    latest_version_id = hub.push(sample_file_path, "pushing sample file", "this is a test for sample file")
    assert latest_version_id is not None

    # create temp dir if not existing
    if not os.path.exists("temp"):
        os.mkdir("temp")

    hub.pull_into("temp", latest_version_id)
    with open(f"temp/{object_id}/{os.path.basename(sample_file_path)}") as file:
        assert file.readlines() == lines

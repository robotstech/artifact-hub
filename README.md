# artifact-hub

![main workflow](https://github.com/robotstech/artifact-hub/actions/workflows/test.yml/badge.svg) <br>

Manage artifacts using object storage. Manage all kinds of artifacts E.g. models, json files, sqlite dbs and track their
versions and history using any object store as a backend. This project facilitates self-hosted hub without a lot of
management overhead.

Currently supported object stores include:

- S3

## Installation

```shell
pip install artifact-hub
```

## Usage

1. Create a sample file `sample.txt`
    ```text
    This is a sample file 
    with multiline content
    ```

2. Initialize the hub instance for a specific object/project
   ```python
   from artifact_hub import s3_hub
   
   hub = s3_hub("bucket", "folder", "object_id")
   hub.push("sample.txt", "first push", "description of first push")
   ```

## Limitations

1. Concurrent push and pulls from multiple parties at the same time can not be handled. because of the linear nature of
   the history the last push will overwrite the previous one.
   ```text
   Actor A and B tries to push concurrently
   Actor A and B pull latest version 10
   Actor A complete push version 11 early
   Actor B completes push version 11 late and overwrite Actor A's push. This may happen when Actor B is pushing a much larger change than A's
   ```
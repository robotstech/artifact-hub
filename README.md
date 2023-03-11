# artifact-hub

Manage artifacts using object storage. Manage all kinds of artifacts E.g. models, json files, sqlite dbs and track their
versions and history using any object store as a backend. This project facilitates self hosted hub without a lot of
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

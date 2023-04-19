# ray-minio-example

This is an exemplary setup to save ray tune checkpoints using minio S3 storage.

``` bash
docker-compose up -d
python minio-example.py
```

## Dependency Versions

```
ray==nightly
pyarrow==6.0.1
aiobotocore==2.5.0
boto3==1.16.52
botocore==1.29.76
```

For minio release, see the image listed in the `docker-compose.yml` file.

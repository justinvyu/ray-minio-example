import boto3
import os

os.environ["AWS_ACCESS_KEY_ID"] = "admin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "myminiopassword"

s3 = boto3.client("s3", endpoint_url="http://localhost:9000")
bucket_name = "checkpoint-bucket"
s3.create_bucket(Bucket=bucket_name)

from ray import air, tune
from ray.air import Checkpoint, session


def train_fn(config):
    print("Let's check!")
    session.report({"data": 1}, checkpoint=Checkpoint.from_dict({"data": 1}))


tuner = tune.Tuner(
    train_fn,
    run_config=air.RunConfig(
        sync_config=tune.SyncConfig(
            upload_dir="s3://checkpoint-bucket?endpoint_override=http://localhost:9000"
        )
    ),
)
results = tuner.fit()
print(results[0].checkpoint.uri)

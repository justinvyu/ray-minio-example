import boto3
import os

env_vars = {"AWS_ACCESS_KEY_ID": "admin", "AWS_SECRET_ACCESS_KEY": "myminiopassword"}

for var in env_vars:
    os.environ[var] = env_vars[var]

# Comment out after the first run. -- START
s3 = boto3.client(
    "s3",
    aws_access_key_id="admin",
    aws_secret_access_key="myminiopassword",
    endpoint_url="http://localhost:9000",
)
bucket_name = "minio-test"
s3.create_bucket(Bucket=bucket_name)
# Comment out after the first run. -- END

from ray import air, tune
from ray.air import Checkpoint, session
import ray

ray.init(runtime_env={"env_vars": env_vars})


def train_fn(config):
    for var in env_vars:
        print(os.environ.get(var))

    session.report({"data": 1}, checkpoint=Checkpoint.from_dict({"data": 1}))


tuner = tune.Tuner(
    train_fn,
    run_config=air.RunConfig(
        storage_path="s3://minio-test?endpoint_override=http://localhost:9000"
    ),
)

results = tuner.fit()
print(results[0].checkpoint.uri)

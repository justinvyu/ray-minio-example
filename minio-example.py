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


class MyTrainable(tune.Trainable):
    def step(self):
        print("step")
        return {"score": 1}

    def save_checkpoint(self, tmp_checkpoint_dir):
        checkpoint_path = os.path.join(tmp_checkpoint_dir, "model.txt")
        with open(checkpoint_path, "w") as f:
            f.write("asdf")
        return checkpoint_path


tuner = tune.Tuner(
    MyTrainable,  # or use train_fn
    run_config=air.RunConfig(
        name="trainable_cls_test",
        storage_path="s3://minio-test?endpoint_override=http://localhost:9000",
        stop={"training_iteration": 1},
    ),
)

results = tuner.fit()
print(results[0].checkpoint.uri)

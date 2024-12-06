import os
from typing import Optional

import boto3

from mind_castle.secret_store_base import SecretStoreBase


class AWSSecretsManagerSecretStore(SecretStoreBase):
    """
    Uses AWS Secrets Manager to store secrets.
    This assumes you have credentials in the environment or in the default AWS credentials file.
    """

    store_type = "awssecretsmanager"
    required_config = [
        [
            "MIND_CASTLE_AWS_REGION",
            "MIND_CASTLE_AWS_ACCESS_KEY_ID",
            "MIND_CASTLE_AWS_SECRET_ACCESS_KEY",
        ],
        ["MIND_CASTLE_AWS_REGION", "MIND_CASTLE_AWS_USE_ENV_AUTH"],
    ]

    def __init__(self):
        if all([os.environ.get(req) for req in self.required_config[0]]):
            # Configure with secret key
            self.client = boto3.client(
                "secretsmanager",
                region_name=os.environ["MIND_CASTLE_AWS_REGION"],
                aws_access_key_id=os.environ["MIND_CASTLE_AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["MIND_CASTLE_AWS_SECRET_ACCESS_KEY"],
            )
        else:
            # Assume the environment is configured with the correct credentials
            self.client = boto3.client(
                "secretsmanager", region_name=os.environ["MIND_CASTLE_AWS_REGION"]
            )

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        response = self.client.get_secret_value(SecretId=key)
        return response.get("SecretString", default)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        # Response is always a success. This throws an exception if it fails
        response = self.client.create_secret(
            Name=key,
            ClientRequestToken=key,
            SecretString=value,
            # Other details we could add:
            # Description='string',
            # KmsKeyId='string',
            # SecretBinary=b'bytes',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # AddReplicaRegions=[
            #     {
            #         'Region': 'string',
            #         'KmsKeyId': 'string'
            #     },
            # ],
            # ForceOverwriteReplicaSecret=True|False
        )

        # ARN is not needed but returned just in case. we could also add tags etc to this response
        return {"secret_type": self.store_type, "key": key, "arn": response.get("ARN")}

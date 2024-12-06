import boto3
from typing import Any
from robot.api.deco import keyword


class s3:
  
    @keyword('S3 Create Bucket')
    def create_bucket(self, bucket_name: str):
        try:
            client = boto3.client('s3')
            client.create_bucket(Bucket=bucket_name)
            return bucket_name
        except Exception as e:
            raise Exception(f"Failed to create bucket {bucket_name}")


    @keyword('S3 Delete Bucket')
    def delete_bucket(self, bucket_name: str):
        try:
            client = boto3.client('s3')
            client.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            raise Exception(f"Failed to delete bucket {bucket_name}")


    @keyword('S3 Should Exists')
    def should_exists(self, bucket_name: str):
        try:
            client = boto3.client('s3')
            client.head_bucket(Bucket=bucket_name)
        except Exception as e:
            raise Exception(f"Bucket {bucket_name} does not exist or does not have permission to access it")

    @keyword('S3 Put Object')
    def put_object(self, bucket_name: str, key: str, data: Any):
        try:
            client = boto3.client('s3')
            client.put_object(Bucket=bucket_name, Key=key, Body=data)
        except Exception as e:
            raise Exception(f"Failed to put object {key} in bucket {bucket_name}")

    @keyword('S3 Delete Object')
    def delete_object(self, bucket_name: str, key: str):
        try:
            client = boto3.client('s3')
            client.delete_object(Bucket=bucket_name, Key=key)
        except Exception as e:
            raise Exception(f"Failed to delete object {key} in bucket {bucket_name}")

    @keyword('S3 Object Should Exists')
    def object_should_exists(self, bucket_name: str, key: str):
        try:
            client = boto3.client('s3')
            client.head_object(Bucket=bucket_name, Key=key)
        except Exception as e:
            raise Exception(f"Object {key} does not exist in bucket {bucket_name}")

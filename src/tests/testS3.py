#!/usr/bin/env python3

import boto3
import pprint

s3 = boto3.client(
    "s3",
    aws_access_key_id="accessKey1",
    aws_secret_access_key="verySecretKey1",
    endpoint_url="http://localhost:8000",
)

s3.create_bucket(Bucket="seau")
print("The current buckets list:")
pprint.PrettyPrinter(indent=2).pprint(s3.list_buckets()['Buckets'])

#!/usr/bin/env python3

# Taken from https://s3-server.readthedocs.io/en/latest/CLIENTS.html#boto3

import boto3

client = boto3.client(
    's3',
    aws_access_key_id='accessKey1',
    aws_secret_access_key='verySecretKey1',
    endpoint_url='http://localhost:8000'
)

client.create_bucket(Bucket='my-bucket')
lists = client.list_buckets()


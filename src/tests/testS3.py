#!/usr/bin/env python3

# Taken from https://s3-server.readthedocs.io/en/latest/CLIENTS.html#boto3

import os

from botocore.utils import fix_s3_host
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = "accessKey1"
os.environ['AWS_SECRET_ACCESS_KEY'] = "verySecretKey1"

s3 = boto3.resource(service_name='s3', endpoint_url='http://localhost:8000')
s3.meta.client.meta.events.unregister('before-sign.s3', fix_s3_host)


for bucket in s3.buckets.all():
    print(bucket.name)



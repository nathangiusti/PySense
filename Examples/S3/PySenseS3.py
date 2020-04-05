import json
import logging
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3', verify=False)
s3_client = boto3.client('s3', verify=False)


def get_buckets():
    """
    Get all s3 buckets  
      
    :return: An array of all s3 buckets   
    """
    bucket_arr = []
    for bucket in s3.buckets.all():
        bucket_arr.append(bucket)
    return bucket_arr


def get_bucket(bucket_name):
    """
    Get an s3 bucket by name   
      
    :param bucket_name: The name of the bucket     
    :return: The s3 bucket  
    """
    return s3.Bucket(bucket_name)


def create_bucket(bucket_name, region=None):
    """
    Creates a new S3 bucket  
      
    :param bucket_name: The bucket name  
    :param region: The region to create the bucket in  
    :return: True if 
    """
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return None
    return True


def upload_dashboard(bucket, dashboard, object_name):
    s3.Object(bucket, object_name).put(Body=(bytes(json.dumps(dashboard).encode('UTF-8'))))


def configure_versioning(bucket_name, version_config):
    bucket = s3.Bucket(bucket_name)
    bucket.configure_versioning(version_config)

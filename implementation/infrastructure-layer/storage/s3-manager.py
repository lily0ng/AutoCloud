#!/usr/bin/env python3
"""S3 Storage Manager"""

import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Manager:
    def __init__(self, region='us-east-1'):
        self.s3 = boto3.client('s3', region_name=region)
        self.region = region
    
    def create_bucket(self, bucket_name):
        """Create S3 bucket"""
        try:
            if self.region == 'us-east-1':
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            logger.info(f"Bucket {bucket_name} created")
            return True
        except ClientError as e:
            logger.error(f"Error creating bucket: {e}")
            return False
    
    def upload_file(self, file_path, bucket_name, object_name=None):
        """Upload file to S3"""
        if object_name is None:
            object_name = file_path
        
        try:
            self.s3.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File {file_path} uploaded to {bucket_name}/{object_name}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def download_file(self, bucket_name, object_name, file_path):
        """Download file from S3"""
        try:
            self.s3.download_file(bucket_name, object_name, file_path)
            logger.info(f"File {object_name} downloaded to {file_path}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return False
    
    def list_objects(self, bucket_name, prefix=''):
        """List objects in bucket"""
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            logger.error(f"Error listing objects: {e}")
            return []
    
    def delete_object(self, bucket_name, object_name):
        """Delete object from S3"""
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Object {object_name} deleted from {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object: {e}")
            return False

if __name__ == "__main__":
    manager = S3Manager()
    print("S3 Manager initialized")

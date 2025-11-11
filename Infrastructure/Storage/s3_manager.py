"""
S3 bucket management
"""
import boto3
from typing import Dict, List


class S3Manager:
    """Manage S3 buckets and objects"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region)
        self.region = region
    
    def create_bucket(self, bucket_name: str, versioning: bool = True, encryption: bool = True):
        """Create S3 bucket with best practices"""
        try:
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            
            # Enable versioning
            if versioning:
                self.s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
            
            # Enable encryption
            if encryption:
                self.s3_client.put_bucket_encryption(
                    Bucket=bucket_name,
                    ServerSideEncryptionConfiguration={
                        'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
                    }
                )
            
            # Block public access
            self.s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            
            return bucket_name
        except Exception as e:
            raise Exception(f"Failed to create bucket: {str(e)}")
    
    def upload_file(self, file_path: str, bucket_name: str, object_key: str):
        """Upload file to S3"""
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            return True
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def download_file(self, bucket_name: str, object_key: str, file_path: str):
        """Download file from S3"""
        try:
            self.s3_client.download_file(bucket_name, object_key, file_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    def set_lifecycle_policy(self, bucket_name: str, rules: List[Dict]):
        """Set lifecycle policy for bucket"""
        try:
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={'Rules': rules}
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to set lifecycle policy: {str(e)}")

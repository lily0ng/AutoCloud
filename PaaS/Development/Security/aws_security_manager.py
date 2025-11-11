import boto3
from typing import Dict, List, Optional
import logging
from datetime import datetime

class AWSSecurityManager:
    def __init__(self, aws_access_key: str, aws_secret_key: str, region: str = 'us-east-1'):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region
        self.logger = logging.getLogger('AWSSecurityManager')

    def get_client(self, service: str):
        return boto3.client(
            service,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )

    def check_ec2_security(self) -> Dict:
        try:
            ec2 = self.get_client('ec2')
            instances = ec2.describe_instances()
            security_status = {
                'unencrypted_volumes': [],
                'public_instances': [],
                'instances_without_tags': []
            }

            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    
                    # Check for public IP
                    if 'PublicIpAddress' in instance:
                        security_status['public_instances'].append(instance_id)
                    
                    # Check for tags
                    if 'Tags' not in instance:
                        security_status['instances_without_tags'].append(instance_id)

            return security_status
        except Exception as e:
            self.logger.error(f"Error checking EC2 security: {str(e)}")
            return {}

    def check_s3_security(self) -> Dict:
        try:
            s3 = self.get_client('s3')
            buckets = s3.list_buckets()['Buckets']
            security_status = {
                'public_buckets': [],
                'unencrypted_buckets': [],
                'versioning_disabled': []
            }

            for bucket in buckets:
                bucket_name = bucket['Name']
                
                # Check bucket ACL
                acl = s3.get_bucket_acl(Bucket=bucket_name)
                for grant in acl['Grants']:
                    if grant['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                        security_status['public_buckets'].append(bucket_name)
                
                # Check encryption
                try:
                    s3.get_bucket_encryption(Bucket=bucket_name)
                except s3.exceptions.ClientError:
                    security_status['unencrypted_buckets'].append(bucket_name)
                
                # Check versioning
                versioning = s3.get_bucket_versioning(Bucket=bucket_name)
                if versioning.get('Status') != 'Enabled':
                    security_status['versioning_disabled'].append(bucket_name)

            return security_status
        except Exception as e:
            self.logger.error(f"Error checking S3 security: {str(e)}")
            return {}

    def enable_security_features(self, resource_id: str, resource_type: str) -> bool:
        try:
            if resource_type == 's3':
                s3 = self.get_client('s3')
                # Enable encryption
                s3.put_bucket_encryption(
                    Bucket=resource_id,
                    ServerSideEncryptionConfiguration={
                        'Rules': [
                            {
                                'ApplyServerSideEncryptionByDefault': {
                                    'SSEAlgorithm': 'AES256'
                                }
                            }
                        ]
                    }
                )
                # Enable versioning
                s3.put_bucket_versioning(
                    Bucket=resource_id,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error enabling security features: {str(e)}")
            return False

    def create_backup(self, resource_id: str, resource_type: str) -> str:
        try:
            if resource_type == 'ec2':
                ec2 = self.get_client('ec2')
                snapshot = ec2.create_snapshot(
                    VolumeId=resource_id,
                    Description=f'Automated backup created on {datetime.now()}'
                )
                return snapshot['SnapshotId']
            return ""
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            return ""

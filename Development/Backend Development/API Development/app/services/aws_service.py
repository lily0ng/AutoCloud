import boto3
from botocore.exceptions import ClientError
from typing import Dict, List
import os

class AWSService:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds')

    async def list_ec2_instances(self) -> List[Dict]:
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'LaunchTime': instance['LaunchTime'].isoformat()
                    })
            return instances
        except ClientError as e:
            raise Exception(f"Error listing EC2 instances: {str(e)}")

    async def list_s3_buckets(self) -> List[Dict]:
        try:
            response = self.s3.list_buckets()
            return [{
                'Name': bucket['Name'],
                'CreationDate': bucket['CreationDate'].isoformat()
            } for bucket in response['Buckets']]
        except ClientError as e:
            raise Exception(f"Error listing S3 buckets: {str(e)}")

    async def create_backup(self, resource_id: str, resource_type: str) -> Dict:
        try:
            if resource_type == 'rds':
                response = self.rds.create_db_snapshot(
                    DBSnapshotIdentifier=f"{resource_id}-snapshot-{int(datetime.now().timestamp())}",
                    DBInstanceIdentifier=resource_id
                )
                return {
                    'SnapshotId': response['DBSnapshot']['DBSnapshotIdentifier'],
                    'Status': response['DBSnapshot']['Status']
                }
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
        except ClientError as e:
            raise Exception(f"Error creating backup: {str(e)}")

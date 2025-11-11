#!/usr/bin/env python3
"""VM/Compute Instance Manager"""

import boto3
from typing import List, Dict

class ComputeManager:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region
    
    def create_instance(self, instance_type='t3.micro', ami_id=None, key_name=None):
        """Create EC2 instance"""
        if not ami_id:
            ami_id = self._get_latest_ami()
        
        response = self.ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'AutoCloud-Instance'}]
            }]
        )
        return response['Instances'][0]['InstanceId']
    
    def list_instances(self) -> List[Dict]:
        """List all instances"""
        response = self.ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'id': instance['InstanceId'],
                    'type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'ip': instance.get('PublicIpAddress', 'N/A')
                })
        return instances
    
    def stop_instance(self, instance_id):
        """Stop instance"""
        self.ec2.stop_instances(InstanceIds=[instance_id])
    
    def start_instance(self, instance_id):
        """Start instance"""
        self.ec2.start_instances(InstanceIds=[instance_id])
    
    def terminate_instance(self, instance_id):
        """Terminate instance"""
        self.ec2.terminate_instances(InstanceIds=[instance_id])
    
    def _get_latest_ami(self):
        """Get latest Amazon Linux AMI"""
        response = self.ec2.describe_images(
            Owners=['amazon'],
            Filters=[
                {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
                {'Name': 'state', 'Values': ['available']}
            ]
        )
        images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        return images[0]['ImageId'] if images else None

if __name__ == "__main__":
    manager = ComputeManager()
    print("Instances:", manager.list_instances())

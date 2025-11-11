#!/usr/bin/env python3

import boto3
import yaml
from botocore.exceptions import ClientError

class AWSIntegration:
    def __init__(self, config_path='config/credentials.yaml'):
        """Initialize AWS API connection"""
        with open(config_path) as f:
            config = yaml.safe_load(f)['aws']
        
        self.ec2 = boto3.client(
            'ec2',
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            region_name=config['region']
        )
        
        self.pricing = boto3.client('pricing', region_name='us-east-1')

    def list_instances(self):
        """List all EC2 instances"""
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                instances.extend(reservation['Instances'])
            return instances
        except ClientError as e:
            print(f"Error listing instances: {e}")
            return []

    def create_instance(self, ami_id, instance_type, key_name, subnet_id=None):
        """Create a new EC2 instance"""
        try:
            run_args = {
                'ImageId': ami_id,
                'InstanceType': instance_type,
                'KeyName': key_name,
                'MinCount': 1,
                'MaxCount': 1
            }
            if subnet_id:
                run_args['SubnetId'] = subnet_id

            response = self.ec2.run_instances(**run_args)
            return response['Instances'][0]
        except ClientError as e:
            print(f"Error creating instance: {e}")
            return None

    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return True
        except ClientError as e:
            print(f"Error stopping instance: {e}")
            return False

    def start_instance(self, instance_id):
        """Start an EC2 instance"""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            return True
        except ClientError as e:
            print(f"Error starting instance: {e}")
            return False

    def terminate_instance(self, instance_id):
        """Terminate an EC2 instance"""
        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            return True
        except ClientError as e:
            print(f"Error terminating instance: {e}")
            return False

    def get_instance_price(self, instance_type, region='us-east-1'):
        """Get the price for an instance type"""
        try:
            response = self.pricing.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                    {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'}
                ]
            )
            return response['PriceList'][0]
        except ClientError as e:
            print(f"Error getting price: {e}")
            return None

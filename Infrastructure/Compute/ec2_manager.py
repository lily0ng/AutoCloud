"""
EC2 instance management
"""
import boto3
from typing import List, Dict


class EC2Manager:
    """Manage EC2 instances"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.ec2_resource = boto3.resource('ec2', region_name=region)
        self.region = region
    
    def launch_instance(self, ami_id: str, instance_type: str, subnet_id: str,
                       security_groups: List[str], key_name: str, name: str,
                       user_data: str = None, iam_role: str = None):
        """Launch EC2 instance"""
        try:
            launch_params = {
                'ImageId': ami_id,
                'InstanceType': instance_type,
                'SubnetId': subnet_id,
                'SecurityGroupIds': security_groups,
                'KeyName': key_name,
                'MinCount': 1,
                'MaxCount': 1,
                'TagSpecifications': [{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': name}]
                }]
            }
            
            if user_data:
                launch_params['UserData'] = user_data
            
            if iam_role:
                launch_params['IamInstanceProfile'] = {'Name': iam_role}
            
            response = self.ec2_client.run_instances(**launch_params)
            return response['Instances'][0]['InstanceId']
        except Exception as e:
            raise Exception(f"Failed to launch instance: {str(e)}")
    
    def stop_instance(self, instance_id: str):
        """Stop EC2 instance"""
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            return True
        except Exception as e:
            raise Exception(f"Failed to stop instance: {str(e)}")
    
    def start_instance(self, instance_id: str):
        """Start EC2 instance"""
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            return True
        except Exception as e:
            raise Exception(f"Failed to start instance: {str(e)}")
    
    def terminate_instance(self, instance_id: str):
        """Terminate EC2 instance"""
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            return True
        except Exception as e:
            raise Exception(f"Failed to terminate instance: {str(e)}")
    
    def get_instance_status(self, instance_id: str):
        """Get instance status"""
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            return {
                'state': instance['State']['Name'],
                'public_ip': instance.get('PublicIpAddress'),
                'private_ip': instance.get('PrivateIpAddress'),
                'instance_type': instance['InstanceType']
            }
        except Exception as e:
            raise Exception(f"Failed to get instance status: {str(e)}")
    
    def create_ami(self, instance_id: str, name: str, description: str = ""):
        """Create AMI from instance"""
        try:
            response = self.ec2_client.create_image(
                InstanceId=instance_id,
                Name=name,
                Description=description,
                NoReboot=True
            )
            return response['ImageId']
        except Exception as e:
            raise Exception(f"Failed to create AMI: {str(e)}")

"""
IAM policy and role management
"""
import boto3
import json
from typing import Dict, List


class IAMPolicyManager:
    """Manage IAM policies and roles"""
    
    def __init__(self):
        self.iam_client = boto3.client('iam')
    
    def create_policy(self, name: str, policy_document: Dict, description: str = ""):
        """Create IAM policy"""
        try:
            response = self.iam_client.create_policy(
                PolicyName=name,
                PolicyDocument=json.dumps(policy_document),
                Description=description
            )
            return response['Policy']['Arn']
        except Exception as e:
            raise Exception(f"Failed to create policy: {str(e)}")
    
    def create_role(self, name: str, assume_role_policy: Dict, description: str = ""):
        """Create IAM role"""
        try:
            response = self.iam_client.create_role(
                RoleName=name,
                AssumeRolePolicyDocument=json.dumps(assume_role_policy),
                Description=description
            )
            return response['Role']['Arn']
        except Exception as e:
            raise Exception(f"Failed to create role: {str(e)}")
    
    def attach_policy_to_role(self, role_name: str, policy_arn: str):
        """Attach policy to role"""
        try:
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to attach policy: {str(e)}")
    
    def create_s3_read_policy(self, bucket_name: str, policy_name: str):
        """Create S3 read-only policy"""
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }]
        }
        return self.create_policy(policy_name, policy_document)
    
    def create_ec2_role(self, role_name: str):
        """Create EC2 instance role"""
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        return self.create_role(role_name, assume_role_policy)
    
    def create_lambda_execution_role(self, role_name: str):
        """Create Lambda execution role"""
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        role_arn = self.create_role(role_name, assume_role_policy)
        
        # Attach basic execution policy
        self.attach_policy_to_role(
            role_name,
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        )
        
        return role_arn

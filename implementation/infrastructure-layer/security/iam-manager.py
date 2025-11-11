#!/usr/bin/env python3
"""IAM Security Manager"""

import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IAMManager:
    def __init__(self):
        self.iam = boto3.client('iam')
    
    def create_role(self, role_name, assume_role_policy):
        """Create IAM role"""
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(assume_role_policy)
            )
            logger.info(f"Role {role_name} created")
            return response['Role']['Arn']
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            return None
    
    def attach_policy(self, role_name, policy_arn):
        """Attach policy to role"""
        try:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            logger.info(f"Policy {policy_arn} attached to {role_name}")
            return True
        except Exception as e:
            logger.error(f"Error attaching policy: {e}")
            return False
    
    def create_user(self, username):
        """Create IAM user"""
        try:
            response = self.iam.create_user(UserName=username)
            logger.info(f"User {username} created")
            return response['User']['Arn']
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def create_access_key(self, username):
        """Create access key for user"""
        try:
            response = self.iam.create_access_key(UserName=username)
            return {
                'access_key_id': response['AccessKey']['AccessKeyId'],
                'secret_access_key': response['AccessKey']['SecretAccessKey']
            }
        except Exception as e:
            logger.error(f"Error creating access key: {e}")
            return None

if __name__ == "__main__":
    manager = IAMManager()
    print("IAM Manager initialized")

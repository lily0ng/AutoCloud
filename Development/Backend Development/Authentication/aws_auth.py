import boto3
import os
from botocore.exceptions import ClientError
from typing import Dict, Optional

class AWSAuthManager:
    def __init__(self):
        self.session = None
        self.credentials = None
        
    def authenticate_with_credentials(self, access_key: str, secret_key: str, region: str = 'us-east-1') -> bool:
        try:
            self.session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            # Verify credentials
            sts = self.session.client('sts')
            sts.get_caller_identity()
            return True
        except ClientError as e:
            print(f"AWS Authentication Error: {str(e)}")
            return False
            
    def authenticate_with_profile(self, profile_name: str) -> bool:
        try:
            self.session = boto3.Session(profile_name=profile_name)
            sts = self.session.client('sts')
            sts.get_caller_identity()
            return True
        except ClientError as e:
            print(f"AWS Profile Authentication Error: {str(e)}")
            return False
            
    def get_session(self) -> Optional[boto3.Session]:
        return self.session
        
    def assume_role(self, role_arn: str, session_name: str) -> Dict:
        try:
            sts_client = self.session.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name
            )
            return assumed_role['Credentials']
        except ClientError as e:
            print(f"Role Assumption Error: {str(e)}")
            return None

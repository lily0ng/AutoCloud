import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import yaml
import boto3
from dotenv import load_dotenv

class SecurityManager:
    def __init__(self):
        load_dotenv()
        self.logger = self._setup_logging()
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('SecurityManager')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_config(self, config_path: str) -> Dict:
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}

    def validate_config(self, config: Dict) -> bool:
        required_fields = ['os_type', 'security_rules', 'monitoring']
        return all(field in config for field in required_fields)

    def get_aws_client(self, service: str):
        return boto3.client(
            service,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region
        )

    def audit_security_groups(self) -> List[Dict]:
        try:
            ec2 = self.get_aws_client('ec2')
            response = ec2.describe_security_groups()
            return response['SecurityGroups']
        except Exception as e:
            self.logger.error(f"Error auditing security groups: {str(e)}")
            return []

    def scan_s3_buckets(self) -> List[Dict]:
        try:
            s3 = self.get_aws_client('s3')
            buckets = s3.list_buckets()['Buckets']
            results = []
            for bucket in buckets:
                bucket_name = bucket['Name']
                encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                results.append({
                    'bucket_name': bucket_name,
                    'creation_date': bucket['CreationDate'],
                    'encryption': encryption.get('ServerSideEncryptionConfiguration', {})
                })
            return results
        except Exception as e:
            self.logger.error(f"Error scanning S3 buckets: {str(e)}")
            return []

    def generate_security_report(self, scan_results: Dict) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_path = f'security_report_{timestamp}.yaml'
        try:
            with open(report_path, 'w') as file:
                yaml.dump(scan_results, file)
            return report_path
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return ""

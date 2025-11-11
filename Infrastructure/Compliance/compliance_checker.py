"""
AWS compliance and security checks
"""
import boto3


class ComplianceChecker:
    """Check AWS resources for compliance"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.config_client = boto3.client('config', region_name=region)
        self.iam_client = boto3.client('iam')
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.region = region
    
    def check_s3_encryption(self):
        """Check if S3 buckets have encryption enabled"""
        try:
            s3_client = boto3.client('s3')
            buckets = s3_client.list_buckets()['Buckets']
            
            non_compliant = []
            for bucket in buckets:
                bucket_name = bucket['Name']
                try:
                    s3_client.get_bucket_encryption(Bucket=bucket_name)
                except:
                    non_compliant.append(bucket_name)
            
            return {'compliant': len(buckets) - len(non_compliant), 'non_compliant': non_compliant}
        except Exception as e:
            raise Exception(f"Failed to check S3 encryption: {str(e)}")
    
    def check_public_instances(self):
        """Check for EC2 instances with public IPs"""
        try:
            response = self.ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            public_instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance.get('PublicIpAddress'):
                        public_instances.append({
                            'instance_id': instance['InstanceId'],
                            'public_ip': instance['PublicIpAddress']
                        })
            
            return public_instances
        except Exception as e:
            raise Exception(f"Failed to check public instances: {str(e)}")

import boto3
from typing import Dict, Any
import logging

class AWSManager:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.logger = logging.getLogger(__name__)

    def create_vpc(self, cidr_block: str) -> Dict[str, Any]:
        try:
            response = self.ec2.create_vpc(CidrBlock=cidr_block)
            vpc_id = response['Vpc']['VpcId']
            self.ec2.create_tags(
                Resources=[vpc_id],
                Tags=[{'Key': 'Name', 'Value': 'PaaS-VPC'}]
            )
            return response
        except Exception as e:
            self.logger.error(f"Failed to create VPC: {str(e)}")
            raise

    def create_ecs_cluster(self, cluster_name: str) -> Dict[str, Any]:
        try:
            return self.ecs.create_cluster(
                clusterName=cluster_name,
                capacityProviders=['FARGATE'],
                defaultCapacityProviderStrategy=[
                    {
                        'capacityProvider': 'FARGATE',
                        'weight': 1
                    }
                ]
            )
        except Exception as e:
            self.logger.error(f"Failed to create ECS cluster: {str(e)}")
            raise

    def create_rds_instance(
        self,
        db_name: str,
        instance_class: str = 'db.t3.micro',
        engine: str = 'postgres'
    ) -> Dict[str, Any]:
        try:
            return self.rds.create_db_instance(
                DBName=db_name,
                DBInstanceIdentifier=f"{db_name}-instance",
                AllocatedStorage=20,
                DBInstanceClass=instance_class,
                Engine=engine,
                MasterUsername='admin',
                MasterUserPassword='temporarypassword123',  # Should be changed immediately
                VpcSecurityGroupIds=[],  # Add security group IDs
                PubliclyAccessible=False
            )
        except Exception as e:
            self.logger.error(f"Failed to create RDS instance: {str(e)}")
            raise

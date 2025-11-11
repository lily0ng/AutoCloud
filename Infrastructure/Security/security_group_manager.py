"""
Security group management
"""
import boto3
from typing import List, Dict


class SecurityGroupManager:
    """Manage AWS security groups"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.region = region
    
    def create_security_group(self, vpc_id: str, name: str, description: str):
        """Create security group"""
        try:
            response = self.ec2_client.create_security_group(
                GroupName=name,
                Description=description,
                VpcId=vpc_id
            )
            return response['GroupId']
        except Exception as e:
            raise Exception(f"Failed to create security group: {str(e)}")
    
    def add_ingress_rule(self, sg_id: str, protocol: str, from_port: int, 
                        to_port: int, cidr: str = None, source_sg: str = None):
        """Add ingress rule to security group"""
        try:
            ip_permissions = [{
                'IpProtocol': protocol,
                'FromPort': from_port,
                'ToPort': to_port
            }]
            
            if cidr:
                ip_permissions[0]['IpRanges'] = [{'CidrIp': cidr}]
            elif source_sg:
                ip_permissions[0]['UserIdGroupPairs'] = [{'GroupId': source_sg}]
            
            self.ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=ip_permissions
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to add ingress rule: {str(e)}")
    
    def add_egress_rule(self, sg_id: str, protocol: str, from_port: int,
                       to_port: int, cidr: str = '0.0.0.0/0'):
        """Add egress rule to security group"""
        try:
            self.ec2_client.authorize_security_group_egress(
                GroupId=sg_id,
                IpPermissions=[{
                    'IpProtocol': protocol,
                    'FromPort': from_port,
                    'ToPort': to_port,
                    'IpRanges': [{'CidrIp': cidr}]
                }]
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to add egress rule: {str(e)}")
    
    def create_web_security_group(self, vpc_id: str, name: str):
        """Create security group for web servers"""
        sg_id = self.create_security_group(vpc_id, name, "Web server security group")
        
        # Allow HTTP
        self.add_ingress_rule(sg_id, 'tcp', 80, 80, '0.0.0.0/0')
        # Allow HTTPS
        self.add_ingress_rule(sg_id, 'tcp', 443, 443, '0.0.0.0/0')
        # Allow SSH (restrict in production)
        self.add_ingress_rule(sg_id, 'tcp', 22, 22, '0.0.0.0/0')
        
        return sg_id
    
    def create_database_security_group(self, vpc_id: str, name: str, app_sg_id: str):
        """Create security group for database servers"""
        sg_id = self.create_security_group(vpc_id, name, "Database security group")
        
        # Allow PostgreSQL from app servers
        self.add_ingress_rule(sg_id, 'tcp', 5432, 5432, source_sg=app_sg_id)
        # Allow MySQL from app servers
        self.add_ingress_rule(sg_id, 'tcp', 3306, 3306, source_sg=app_sg_id)
        
        return sg_id

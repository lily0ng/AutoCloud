"""
VPC management and configuration
"""
import boto3
from typing import List, Dict


class VPCManager:
    """Manage AWS VPC resources"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.region = region
    
    def create_vpc(self, cidr_block: str, name: str, enable_dns: bool = True):
        """Create VPC"""
        try:
            response = self.ec2_client.create_vpc(
                CidrBlock=cidr_block,
                AmazonProvidedIpv6CidrBlock=False
            )
            vpc_id = response['Vpc']['VpcId']
            
            # Enable DNS
            if enable_dns:
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsHostnames={'Value': True}
                )
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsSupport={'Value': True}
                )
            
            # Tag VPC
            self.ec2_client.create_tags(
                Resources=[vpc_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            return vpc_id
        except Exception as e:
            raise Exception(f"Failed to create VPC: {str(e)}")
    
    def create_subnet(self, vpc_id: str, cidr_block: str, az: str, 
                     name: str, public: bool = False):
        """Create subnet"""
        try:
            response = self.ec2_client.create_subnet(
                VpcId=vpc_id,
                CidrBlock=cidr_block,
                AvailabilityZone=az
            )
            subnet_id = response['Subnet']['SubnetId']
            
            # Enable auto-assign public IP for public subnets
            if public:
                self.ec2_client.modify_subnet_attribute(
                    SubnetId=subnet_id,
                    MapPublicIpOnLaunch={'Value': True}
                )
            
            # Tag subnet
            self.ec2_client.create_tags(
                Resources=[subnet_id],
                Tags=[
                    {'Key': 'Name', 'Value': name},
                    {'Key': 'Type', 'Value': 'Public' if public else 'Private'}
                ]
            )
            
            return subnet_id
        except Exception as e:
            raise Exception(f"Failed to create subnet: {str(e)}")
    
    def create_internet_gateway(self, vpc_id: str, name: str):
        """Create and attach internet gateway"""
        try:
            response = self.ec2_client.create_internet_gateway()
            igw_id = response['InternetGateway']['InternetGatewayId']
            
            # Attach to VPC
            self.ec2_client.attach_internet_gateway(
                InternetGatewayId=igw_id,
                VpcId=vpc_id
            )
            
            # Tag IGW
            self.ec2_client.create_tags(
                Resources=[igw_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            return igw_id
        except Exception as e:
            raise Exception(f"Failed to create internet gateway: {str(e)}")
    
    def create_nat_gateway(self, subnet_id: str, name: str):
        """Create NAT gateway"""
        try:
            # Allocate Elastic IP
            eip_response = self.ec2_client.allocate_address(Domain='vpc')
            allocation_id = eip_response['AllocationId']
            
            # Create NAT Gateway
            response = self.ec2_client.create_nat_gateway(
                SubnetId=subnet_id,
                AllocationId=allocation_id
            )
            nat_gw_id = response['NatGateway']['NatGatewayId']
            
            # Tag NAT Gateway
            self.ec2_client.create_tags(
                Resources=[nat_gw_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            return nat_gw_id
        except Exception as e:
            raise Exception(f"Failed to create NAT gateway: {str(e)}")
    
    def create_route_table(self, vpc_id: str, name: str, routes: List[Dict] = None):
        """Create route table"""
        try:
            response = self.ec2_client.create_route_table(VpcId=vpc_id)
            route_table_id = response['RouteTable']['RouteTableId']
            
            # Add routes
            if routes:
                for route in routes:
                    self.ec2_client.create_route(
                        RouteTableId=route_table_id,
                        **route
                    )
            
            # Tag route table
            self.ec2_client.create_tags(
                Resources=[route_table_id],
                Tags=[{'Key': 'Name', 'Value': name}]
            )
            
            return route_table_id
        except Exception as e:
            raise Exception(f"Failed to create route table: {str(e)}")

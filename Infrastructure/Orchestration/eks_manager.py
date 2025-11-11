"""
EKS cluster management
"""
import boto3
from typing import List


class EKSManager:
    """Manage EKS clusters"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.eks_client = boto3.client('eks', region_name=region)
        self.region = region
    
    def create_cluster(self, cluster_name: str, role_arn: str, subnet_ids: List[str],
                      security_group_ids: List[str], version: str = '1.28'):
        """Create EKS cluster"""
        try:
            response = self.eks_client.create_cluster(
                name=cluster_name,
                version=version,
                roleArn=role_arn,
                resourcesVpcConfig={
                    'subnetIds': subnet_ids,
                    'securityGroupIds': security_group_ids,
                    'endpointPublicAccess': True,
                    'endpointPrivateAccess': True
                },
                logging={
                    'clusterLogging': [{
                        'types': ['api', 'audit', 'authenticator', 'controllerManager', 'scheduler'],
                        'enabled': True
                    }]
                }
            )
            return response['cluster']['name']
        except Exception as e:
            raise Exception(f"Failed to create cluster: {str(e)}")
    
    def create_node_group(self, cluster_name: str, node_group_name: str,
                         node_role_arn: str, subnet_ids: List[str],
                         instance_types: List[str], desired_size: int = 2,
                         min_size: int = 1, max_size: int = 4):
        """Create EKS node group"""
        try:
            response = self.eks_client.create_nodegroup(
                clusterName=cluster_name,
                nodegroupName=node_group_name,
                scalingConfig={
                    'minSize': min_size,
                    'maxSize': max_size,
                    'desiredSize': desired_size
                },
                subnets=subnet_ids,
                instanceTypes=instance_types,
                nodeRole=node_role_arn,
                amiType='AL2_x86_64',
                diskSize=20
            )
            return response['nodegroup']['nodegroupName']
        except Exception as e:
            raise Exception(f"Failed to create node group: {str(e)}")
    
    def get_cluster_status(self, cluster_name: str):
        """Get cluster status"""
        try:
            response = self.eks_client.describe_cluster(name=cluster_name)
            return {
                'status': response['cluster']['status'],
                'endpoint': response['cluster']['endpoint'],
                'version': response['cluster']['version']
            }
        except Exception as e:
            raise Exception(f"Failed to get cluster status: {str(e)}")

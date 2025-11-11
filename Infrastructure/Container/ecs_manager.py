"""
ECS cluster and service management
"""
import boto3
from typing import List, Dict
import json


class ECSManager:
    """Manage ECS clusters and services"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ecs_client = boto3.client('ecs', region_name=region)
        self.region = region
    
    def create_cluster(self, cluster_name: str):
        """Create ECS cluster"""
        try:
            response = self.ecs_client.create_cluster(
                clusterName=cluster_name,
                settings=[{'name': 'containerInsights', 'value': 'enabled'}]
            )
            return response['cluster']['clusterArn']
        except Exception as e:
            raise Exception(f"Failed to create cluster: {str(e)}")
    
    def register_task_definition(self, family: str, container_definitions: List[Dict],
                                 cpu: str = '256', memory: str = '512',
                                 execution_role_arn: str = None):
        """Register ECS task definition"""
        try:
            params = {
                'family': family,
                'networkMode': 'awsvpc',
                'requiresCompatibilities': ['FARGATE'],
                'cpu': cpu,
                'memory': memory,
                'containerDefinitions': container_definitions
            }
            
            if execution_role_arn:
                params['executionRoleArn'] = execution_role_arn
            
            response = self.ecs_client.register_task_definition(**params)
            return response['taskDefinition']['taskDefinitionArn']
        except Exception as e:
            raise Exception(f"Failed to register task definition: {str(e)}")
    
    def create_service(self, cluster: str, service_name: str, task_definition: str,
                      desired_count: int, subnets: List[str], security_groups: List[str],
                      target_group_arn: str = None):
        """Create ECS service"""
        try:
            params = {
                'cluster': cluster,
                'serviceName': service_name,
                'taskDefinition': task_definition,
                'desiredCount': desired_count,
                'launchType': 'FARGATE',
                'networkConfiguration': {
                    'awsvpcConfiguration': {
                        'subnets': subnets,
                        'securityGroups': security_groups,
                        'assignPublicIp': 'ENABLED'
                    }
                }
            }
            
            if target_group_arn:
                params['loadBalancers'] = [{
                    'targetGroupArn': target_group_arn,
                    'containerName': service_name,
                    'containerPort': 80
                }]
            
            response = self.ecs_client.create_service(**params)
            return response['service']['serviceArn']
        except Exception as e:
            raise Exception(f"Failed to create service: {str(e)}")
    
    def update_service(self, cluster: str, service: str, desired_count: int = None,
                      task_definition: str = None):
        """Update ECS service"""
        try:
            params = {'cluster': cluster, 'service': service}
            
            if desired_count is not None:
                params['desiredCount'] = desired_count
            
            if task_definition:
                params['taskDefinition'] = task_definition
            
            response = self.ecs_client.update_service(**params)
            return response['service']['serviceArn']
        except Exception as e:
            raise Exception(f"Failed to update service: {str(e)}")

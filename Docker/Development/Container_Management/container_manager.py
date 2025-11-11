#!/usr/bin/env python3

import os
import sys
import click
import docker
import boto3
import yaml
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
docker_client = docker.from_env()
aws_session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
ecs_client = aws_session.client('ecs')
ecr_client = aws_session.client('ecr')

class ContainerManager:
    def __init__(self):
        self.docker_client = docker_client
        self.ecs_client = ecs_client
        self.ecr_client = ecr_client

    def list_local_containers(self):
        """List all local Docker containers"""
        table = Table(title="Local Docker Containers")
        table.add_column("Container ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Image", style="blue")

        containers = self.docker_client.containers.list(all=True)
        for container in containers:
            table.add_row(
                container.short_id,
                container.name,
                container.status,
                container.image.tags[0] if container.image.tags else "none"
            )
        console.print(table)

    def list_ecs_clusters(self):
        """List ECS clusters"""
        table = Table(title="AWS ECS Clusters")
        table.add_column("Cluster Name", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_column("Active Services", style="green")

        clusters = self.ecs_client.list_clusters()['clusterArns']
        for cluster in clusters:
            cluster_name = cluster.split('/')[-1]
            details = self.ecs_client.describe_clusters(clusters=[cluster])['clusters'][0]
            services = len(self.ecs_client.list_services(cluster=cluster_name)['serviceArns'])
            table.add_row(
                cluster_name,
                details['status'],
                str(services)
            )
        console.print(table)

    def manage_local_container(self, action, container_id):
        """Manage local Docker container"""
        try:
            container = self.docker_client.containers.get(container_id)
            if action == 'start':
                container.start()
                console.print(f"[green]Started container {container_id}")
            elif action == 'stop':
                container.stop()
                console.print(f"[yellow]Stopped container {container_id}")
            elif action == 'remove':
                container.remove(force=True)
                console.print(f"[red]Removed container {container_id}")
        except docker.errors.NotFound:
            console.print(f"[red]Container {container_id} not found")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}")

    def deploy_to_ecs(self, task_definition, cluster_name):
        """Deploy container to ECS"""
        try:
            response = self.ecs_client.run_task(
                cluster=cluster_name,
                taskDefinition=task_definition,
                count=1,
                launchType='FARGATE',
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': [os.getenv('AWS_SUBNET_ID')],
                        'securityGroups': [os.getenv('AWS_SECURITY_GROUP')],
                        'assignPublicIp': 'ENABLED'
                    }
                }
            )
            console.print(f"[green]Deployed task to ECS cluster {cluster_name}")
            return response
        except Exception as e:
            console.print(f"[red]Error deploying to ECS: {str(e)}")

    def push_to_ecr(self, image_name, repository_name):
        """Push Docker image to ECR"""
        try:
            # Get ECR login token
            token = self.ecr_client.get_authorization_token()
            username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
            registry = token['authorizationData'][0]['proxyEndpoint']

            # Login to ECR
            self.docker_client.login(username=username, password=password, registry=registry)

            # Tag and push image
            local_image = self.docker_client.images.get(image_name)
            ecr_repo_uri = f"{registry}/{repository_name}"
            local_image.tag(ecr_repo_uri)
            
            for line in self.docker_client.images.push(ecr_repo_uri, stream=True, decode=True):
                console.print(line)
            
            console.print(f"[green]Successfully pushed {image_name} to ECR")
        except Exception as e:
            console.print(f"[red]Error pushing to ECR: {str(e)}")

    def monitor_resources(self):
        """Monitor container resources"""
        table = Table(title="Container Resource Usage")
        table.add_column("Container ID", style="cyan")
        table.add_column("CPU %", style="yellow")
        table.add_column("Memory Usage", style="green")
        table.add_column("Network I/O", style="blue")

        for container in self.docker_client.containers.list():
            stats = container.stats(stream=False)
            cpu_percent = self._calculate_cpu_percent(stats)
            memory_usage = self._calculate_memory_usage(stats)
            network_io = self._calculate_network_io(stats)

            table.add_row(
                container.short_id,
                f"{cpu_percent:.2f}%",
                memory_usage,
                network_io
            )
        console.print(table)

    def _calculate_cpu_percent(self, stats):
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                      stats["precpu_stats"]["system_cpu_usage"]
        return (cpu_delta / system_delta) * 100.0

    def _calculate_memory_usage(self, stats):
        usage = stats["memory_stats"]["usage"]
        return f"{usage / (1024*1024):.2f} MB"

    def _calculate_network_io(self, stats):
        rx_bytes = stats["networks"]["eth0"]["rx_bytes"]
        tx_bytes = stats["networks"]["eth0"]["tx_bytes"]
        return f"↓{rx_bytes/(1024*1024):.2f}MB ↑{tx_bytes/(1024*1024):.2f}MB"

@click.group()
def cli():
    """Container Management CLI"""
    pass

@cli.command()
def list_containers():
    """List all Docker containers"""
    manager = ContainerManager()
    manager.list_local_containers()

@cli.command()
def list_clusters():
    """List ECS clusters"""
    manager = ContainerManager()
    manager.list_ecs_clusters()

@cli.command()
@click.argument('action', type=click.Choice(['start', 'stop', 'remove']))
@click.argument('container_id')
def container(action, container_id):
    """Manage Docker container"""
    manager = ContainerManager()
    manager.manage_local_container(action, container_id)

@cli.command()
@click.argument('task_definition')
@click.argument('cluster_name')
def deploy_ecs(task_definition, cluster_name):
    """Deploy to ECS"""
    manager = ContainerManager()
    manager.deploy_to_ecs(task_definition, cluster_name)

@cli.command()
@click.argument('image_name')
@click.argument('repository_name')
def push_ecr(image_name, repository_name):
    """Push image to ECR"""
    manager = ContainerManager()
    manager.push_to_ecr(image_name, repository_name)

@cli.command()
def monitor():
    """Monitor container resources"""
    manager = ContainerManager()
    manager.monitor_resources()

if __name__ == '__main__':
    cli()

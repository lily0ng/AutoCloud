#!/usr/bin/env python3

import boto3
import click
import yaml
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSBackupManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.ec2 = boto3.client('ec2', region_name=self.config['regions']['primary'])
        self.ec2_dr = boto3.client('ec2', region_name=self.config['regions']['dr'])

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_snapshot(self, instance_id: str, volume_id: str, description: str) -> Dict:
        """Create an EBS snapshot."""
        try:
            snapshot = self.ec2.create_snapshot(
                VolumeId=volume_id,
                Description=description
            )
            
            # Add tags
            instance_config = self._get_instance_config(instance_id)
            if instance_config:
                self.ec2.create_tags(
                    Resources=[snapshot['SnapshotId']],
                    Tags=[{'Key': k, 'Value': v} for k, v in instance_config.get('tags', {}).items()]
                )
            
            return snapshot
        except ClientError as e:
            logger.error(f"Failed to create snapshot: {str(e)}")
            raise

    def copy_snapshot_to_dr(self, snapshot_id: str) -> Dict:
        """Copy snapshot to DR region."""
        try:
            response = self.ec2_dr.copy_snapshot(
                SourceRegion=self.config['regions']['primary'],
                SourceSnapshotId=snapshot_id,
                Encrypted=self.config['encryption']['enabled'],
                KmsKeyId=self.config['encryption']['cross_region_key_id']
            )
            return response
        except ClientError as e:
            logger.error(f"Failed to copy snapshot to DR: {str(e)}")
            raise

    def cleanup_snapshots(self, backup_group: str):
        """Clean up old snapshots based on retention policy."""
        try:
            retention = self.config['snapshot_policies'][backup_group]['retention']
            
            # Get all snapshots for this backup group
            snapshots = self.ec2.describe_snapshots(
                Filters=[
                    {'Name': 'tag:BackupGroup', 'Values': [backup_group]}
                ]
            )['Snapshots']
            
            # Sort snapshots by date
            snapshots.sort(key=lambda x: x['StartTime'])
            
            # Calculate retention dates
            now = datetime.utcnow()
            retention_dates = {
                'hourly': now - timedelta(hours=retention.get('hourly', 24)),
                'daily': now - timedelta(days=retention.get('daily', 7)),
                'weekly': now - timedelta(weeks=retention.get('weekly', 4)),
                'monthly': now - timedelta(days=retention.get('monthly', 12) * 30)
            }
            
            # Delete expired snapshots
            for snapshot in snapshots:
                if snapshot['StartTime'] < retention_dates['monthly']:
                    self.ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    logger.info(f"Deleted snapshot {snapshot['SnapshotId']}")
                    
        except ClientError as e:
            logger.error(f"Failed to cleanup snapshots: {str(e)}")
            raise

    def create_volume_from_snapshot(self, snapshot_id: str, availability_zone: str, 
                                  volume_type: str = 'gp3') -> Dict:
        """Create a new volume from snapshot."""
        try:
            volume = self.ec2.create_volume(
                SnapshotId=snapshot_id,
                AvailabilityZone=availability_zone,
                VolumeType=volume_type
            )
            
            # Wait for volume to be available
            waiter = self.ec2.get_waiter('volume_available')
            waiter.wait(VolumeIds=[volume['VolumeId']])
            
            return volume
        except ClientError as e:
            logger.error(f"Failed to create volume: {str(e)}")
            raise

    def attach_volume(self, volume_id: str, instance_id: str, device: str):
        """Attach volume to instance."""
        try:
            self.ec2.attach_volume(
                VolumeId=volume_id,
                InstanceId=instance_id,
                Device=device
            )
            
            # Wait for attachment
            waiter = self.ec2.get_waiter('volume_in_use')
            waiter.wait(VolumeIds=[volume_id])
            
        except ClientError as e:
            logger.error(f"Failed to attach volume: {str(e)}")
            raise

    def _get_instance_config(self, instance_id: str) -> Dict:
        """Get instance configuration from config file."""
        for env in ['production', 'staging']:
            for instance in self.config['instances'].get(env, []):
                if instance['id'] == instance_id:
                    return instance
        return None

@click.group()
def cli():
    """AWS Backup Management CLI"""
    pass

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.option('--volume-id', required=True, help='EBS volume ID')
@click.option('--description', default='', help='Snapshot description')
def create_backup(config, instance_id, volume_id, description):
    """Create backup for an EC2 instance volume."""
    manager = AWSBackupManager(config)
    snapshot = manager.create_snapshot(instance_id, volume_id, description)
    click.echo(f"Created snapshot: {snapshot['SnapshotId']}")

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--snapshot-id', required=True, help='Snapshot ID')
@click.option('--availability-zone', required=True, help='Target availability zone')
@click.option('--instance-id', required=True, help='Target instance ID')
@click.option('--device', required=True, help='Device name (e.g., /dev/xvdf)')
def restore(config, snapshot_id, availability_zone, instance_id, device):
    """Restore a volume from snapshot and attach to instance."""
    manager = AWSBackupManager(config)
    volume = manager.create_volume_from_snapshot(snapshot_id, availability_zone)
    click.echo(f"Created volume: {volume['VolumeId']}")
    
    manager.attach_volume(volume['VolumeId'], instance_id, device)
    click.echo(f"Attached volume to instance {instance_id}")

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--backup-group', required=True, help='Backup group name')
def cleanup(config, backup_group):
    """Clean up old snapshots based on retention policy."""
    manager = AWSBackupManager(config)
    manager.cleanup_snapshots(backup_group)
    click.echo("Cleanup completed")

if __name__ == '__main__':
    cli()

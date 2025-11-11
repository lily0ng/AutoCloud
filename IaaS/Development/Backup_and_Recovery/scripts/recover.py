#!/usr/bin/env python3

import os
import sys
import yaml
import click
import logging
import boto3
import libvirt
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecoveryManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.platform = self.config['platform']
        self.recovery_handlers = {
            'ubuntu': self._recover_ubuntu,
            'centos': self._recover_centos,
            'rocky': self._recover_rocky,
            'aws': self._recover_aws,
            'kvm': self._recover_kvm
        }

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return self._resolve_env_vars(config)

    def _resolve_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve environment variables in config values."""
        def _resolve(value):
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                return os.environ.get(env_var, '')
            return value

        def _traverse(obj):
            if isinstance(obj, dict):
                return {k: _traverse(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_traverse(v) for v in obj]
            return _resolve(obj)

        return _traverse(config)

    def _recover_ubuntu(self, backup_date: str, target_dir: str = "/"):
        """Recover Ubuntu system from backup."""
        logger.info(f"Starting Ubuntu recovery process to {target_dir}")
        try:
            s3 = boto3.client('s3')
            bucket = self.config['storage']['bucket']
            prefix = self.config['storage']['prefix']
            
            # List available backups
            backups = self._list_s3_backups(bucket, prefix)
            backup_file = next((b for b in backups if backup_date in b), None)
            
            if not backup_file:
                raise ValueError(f"No backup found for date: {backup_date}")

            # Download backup
            temp_dir = "/tmp/recovery"
            os.makedirs(temp_dir, exist_ok=True)
            local_backup = f"{temp_dir}/backup.tar.gz"
            
            s3.download_file(bucket, backup_file, local_backup)
            
            # Extract backup
            os.system(f"tar xzf {local_backup} -C {target_dir}")
            
            logger.info("Recovery completed successfully")
            
        except Exception as e:
            logger.error(f"Recovery failed: {str(e)}")
            raise

    def _recover_aws(self, snapshot_id: str, volume_id: str = None):
        """Recover AWS instance from snapshot."""
        logger.info("Starting AWS recovery process")
        try:
            ec2 = boto3.client('ec2')
            
            # Verify snapshot exists
            snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])['Snapshots'][0]
            
            if volume_id:
                # Create new volume from snapshot
                new_volume = ec2.create_volume(
                    SnapshotId=snapshot_id,
                    AvailabilityZone=snapshot['AvailabilityZone'],
                    VolumeType='gp3'
                )
                
                # Wait for volume to be available
                waiter = ec2.get_waiter('volume_available')
                waiter.wait(VolumeIds=[new_volume['VolumeId']])
                
                logger.info(f"Created new volume: {new_volume['VolumeId']}")
                
                # Attach volume to instance
                if volume_id:
                    ec2.attach_volume(
                        VolumeId=new_volume['VolumeId'],
                        InstanceId=self.config['backup']['instances'][0]['id'],
                        Device=volume_id
                    )
            
        except Exception as e:
            logger.error(f"AWS recovery failed: {str(e)}")
            raise

    def _recover_kvm(self, snapshot_name: str, domain_name: str):
        """Recover KVM virtual machine from snapshot."""
        logger.info(f"Starting KVM recovery for domain {domain_name}")
        try:
            conn = libvirt.open("qemu:///system")
            if conn is None:
                raise Exception("Failed to connect to KVM/QEMU")

            domain = conn.lookupByName(domain_name)
            if domain is None:
                raise Exception(f"Domain {domain_name} not found")

            snapshots = domain.listAllSnapshots()
            target_snapshot = next((s for s in snapshots if s.getName() == snapshot_name), None)
            
            if not target_snapshot:
                raise ValueError(f"Snapshot {snapshot_name} not found")

            # Revert to snapshot
            domain.revertToSnapshot(target_snapshot)
            
            logger.info(f"Successfully reverted {domain_name} to snapshot {snapshot_name}")
            
        except Exception as e:
            logger.error(f"KVM recovery failed: {str(e)}")
            raise

    def _list_s3_backups(self, bucket: str, prefix: str) -> List[str]:
        """List available backups in S3."""
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj['Key'] for obj in response.get('Contents', [])]

    def run_recovery(self, **kwargs):
        """Run recovery for the configured platform."""
        handler = self.recovery_handlers.get(self.platform)
        if not handler:
            raise ValueError(f"Unsupported platform: {self.platform}")
        
        handler(**kwargs)

@click.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--backup-date', required=True, help='Date of backup to recover (YYYYMMDD-HHMMSS)')
@click.option('--target-dir', default="/", help='Target directory for recovery (Ubuntu/CentOS)')
@click.option('--snapshot-id', help='Snapshot ID (AWS)')
@click.option('--volume-id', help='Volume ID (AWS)')
@click.option('--domain-name', help='Domain name (KVM)')
def main(config, backup_date, target_dir, snapshot_id, volume_id, domain_name):
    """Main recovery script."""
    try:
        recovery_manager = RecoveryManager(config)
        recovery_manager.run_recovery(
            backup_date=backup_date,
            target_dir=target_dir,
            snapshot_id=snapshot_id,
            volume_id=volume_id,
            domain_name=domain_name
        )
    except Exception as e:
        logger.error(f"Recovery failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

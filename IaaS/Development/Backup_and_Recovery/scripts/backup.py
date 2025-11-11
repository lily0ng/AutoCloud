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
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.platform = self.config['platform']
        self.backup_handlers = {
            'ubuntu': self._backup_ubuntu,
            'centos': self._backup_centos,
            'rocky': self._backup_rocky,
            'aws': self._backup_aws,
            'kvm': self._backup_kvm
                            
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

    def _backup_ubuntu(self):
        logger.info("Starting Ubuntu backup process")
        try:
            dirs = self.config['backup']['directories']
            exclude = self.config['backup'].get('exclude', [])
            
            backup_path = f"/tmp/backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            os.makedirs(backup_path, exist_ok=True)

            for directory in dirs:
                if not os.path.exists(directory):
                    logger.warning(f"Directory {directory} does not exist, skipping...")
                    continue
                
                backup_cmd = f"rsync -az --delete"
                for exc in exclude:
                    backup_cmd += f" --exclude='{exc}'"
                backup_cmd += f" {directory} {backup_path}/"
                
                os.system(backup_cmd)

            if self.config['compression']['enabled']:
                compression_level = self.config['compression']['level']
                os.system(f"tar czf {backup_path}.tar.gz -C {backup_path} .")

            if self.config['storage']['type'] == 's3':
                self._upload_to_s3(f"{backup_path}.tar.gz")

        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            self._send_notification("Backup failed", str(e))
            raise

    def _backup_aws(self):
        logger.info("Starting AWS backup process")
        try:
            session = boto3.Session()
            ec2 = session.client('ec2')
            
            for instance in self.config['backup']['instances']:
                instance_id = instance['id']
                
                # Create snapshot for each volume
                for volume_id in instance['volumes']:
                    snapshot = ec2.create_snapshot(
                        VolumeId=volume_id,
                        Description=f"Automated backup {datetime.now().isoformat()}"
                    )
                    
                    # Tag the snapshot
                    ec2.create_tags(
                        Resources=[snapshot['SnapshotId']],
                        Tags=[{'Key': k, 'Value': v} for k, v in self.config['tags'].items()]
                    )

                    if self.config['backup']['snapshot']['enabled']:
                        self._copy_snapshot_to_dr(snapshot['SnapshotId'])

        except Exception as e:
            logger.error(f"AWS backup failed: {str(e)}")
            self._send_notification("AWS backup failed", str(e))
            raise

    def _backup_kvm(self):
        logger.info("Starting KVM backup process")
        try:
            conn = libvirt.open("qemu:///system")
            if conn is None:
                raise Exception("Failed to connect to KVM/QEMU")

            domains = conn.listAllDomains()
            for domain in domains:
                if domain.isActive():
                    # Create snapshot
                    xml = domain.snapshotCreateXML(
                        f"""
                        <domainsnapshot>
                            <name>backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}</name>
                            <description>Automated backup</description>
                        </domainsnapshot>
                        """
                    )

        except Exception as e:
            logger.error(f"KVM backup failed: {str(e)}")
            self._send_notification("KVM backup failed", str(e))
            raise

    def _upload_to_s3(self, file_path: str):
        """Upload backup to S3."""
        s3 = boto3.client('s3')
        bucket = self.config['storage']['bucket']
        prefix = self.config['storage']['prefix']
        key = f"{prefix}/{Path(file_path).name}"
        
        s3.upload_file(file_path, bucket, key)

    def _send_notification(self, subject: str, message: str):
        """Send notification about backup status."""
        if not self.config['notification']['enabled']:
            return

        if self.config['notification']['type'] == 'email':
            # Implement email notification
            pass
        elif self.config['notification']['type'] == 'sns':
            sns = boto3.client('sns')
            sns.publish(
                TopicArn=self.config['notification']['sns_topic'],
                Subject=subject,
                Message=message
            )

    def run_backup(self):
        """Run backup for the configured platform."""
        handler = self.backup_handlers.get(self.platform)
        if not handler:
            raise ValueError(f"Unsupported platform: {self.platform}")
        
        handler()

@click.command()
@click.option('--config', '-c', required=True, help='Path to config file')
def main(config):
    """Main backup script."""
    try:
        backup_manager = BackupManager(config)
        backup_manager.run_backup()
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

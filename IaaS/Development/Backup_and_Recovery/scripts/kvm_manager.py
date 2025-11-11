#!/usr/bin/env python3

import libvirt
import click
import yaml
import logging
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Any
from xml.etree import ElementTree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KVMBackupManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.conn = libvirt.open(self.config['hypervisor']['uri'])
        if self.conn is None:
            raise Exception("Failed to connect to KVM/QEMU")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_snapshot(self, domain_name: str, snapshot_name: str = None) -> str:
        """Create a snapshot of a VM."""
        try:
            domain = self.conn.lookupByName(domain_name)
            if domain is None:
                raise Exception(f"Domain {domain_name} not found")

            vm_config = self._get_vm_config(domain_name)
            if not vm_config:
                raise Exception(f"Configuration for {domain_name} not found")

            if snapshot_name is None:
                snapshot_name = f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            # Prepare snapshot XML
            snapshot_xml = f"""
            <domainsnapshot>
                <name>{snapshot_name}</name>
                <description>Automated backup</description>
                <memory snapshot='{vm_config['backup_type']}' file='{self._get_memory_path(domain_name, snapshot_name)}'/>
                <disks>
            """

            # Add disk configurations
            for disk in vm_config['disks']:
                if disk['backup']:
                    snapshot_xml += f"""
                    <disk name='{disk['path']}'>
                        <source file='{self._get_disk_snapshot_path(disk['path'], snapshot_name)}'/>
                    </disk>
                    """

            snapshot_xml += """
                </disks>
            </domainsnapshot>
            """

            # Create snapshot
            snapshot = domain.snapshotCreateXML(snapshot_xml, 
                                              libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY)
            
            return snapshot.getName()

        except libvirt.libvirtError as e:
            logger.error(f"Failed to create snapshot: {str(e)}")
            raise

    def backup_to_remote(self, domain_name: str, snapshot_name: str):
        """Copy snapshot to remote storage."""
        try:
            if not self.config['storage']['remote']['enabled']:
                return

            remote_path = self.config['storage']['remote']['path']
            
            # Ensure remote directory exists
            remote_dir = os.path.join(remote_path, domain_name, snapshot_name)
            os.makedirs(remote_dir, exist_ok=True)

            # Copy memory state if exists
            memory_path = self._get_memory_path(domain_name, snapshot_name)
            if os.path.exists(memory_path):
                self._copy_to_remote(memory_path, remote_dir)

            # Copy disk snapshots
            vm_config = self._get_vm_config(domain_name)
            for disk in vm_config['disks']:
                if disk['backup']:
                    disk_snapshot = self._get_disk_snapshot_path(disk['path'], snapshot_name)
                    self._copy_to_remote(disk_snapshot, remote_dir)

        except Exception as e:
            logger.error(f"Failed to backup to remote: {str(e)}")
            raise

    def restore_snapshot(self, domain_name: str, snapshot_name: str):
        """Restore a VM from snapshot."""
        try:
            domain = self.conn.lookupByName(domain_name)
            if domain is None:
                raise Exception(f"Domain {domain_name} not found")

            vm_config = self._get_vm_config(domain_name)
            if not vm_config:
                raise Exception(f"Configuration for {domain_name} not found")

            # If cold backup, ensure VM is shutdown
            if vm_config['backup_type'] == 'cold' and domain.isActive():
                domain.shutdown()
                # Wait for shutdown
                while domain.isActive():
                    time.sleep(1)

            # Find snapshot
            snapshot = domain.snapshotLookupByName(snapshot_name)
            if snapshot is None:
                raise Exception(f"Snapshot {snapshot_name} not found")

            # Revert to snapshot
            domain.revertToSnapshot(snapshot)

            # Start VM if it was running
            if vm_config['backup_type'] == 'cold':
                domain.create()

        except libvirt.libvirtError as e:
            logger.error(f"Failed to restore snapshot: {str(e)}")
            raise

    def verify_backup(self, domain_name: str, snapshot_name: str):
        """Verify backup integrity."""
        try:
            vm_config = self._get_vm_config(domain_name)
            if not vm_config:
                raise Exception(f"Configuration for {domain_name} not found")

            # Create test VM
            test_xml = self._create_test_vm_xml(domain_name, snapshot_name)
            test_domain = self.conn.defineXML(test_xml)

            # Start test VM
            test_domain.create()

            # Wait for boot timeout
            timeout = self.config['recovery']['verification']['timeout']
            time.sleep(timeout)

            # Check if VM is running
            if not test_domain.isActive():
                raise Exception("Test VM failed to boot")

            # Cleanup test VM
            test_domain.destroy()
            test_domain.undefine()

            logger.info(f"Backup verification successful for {domain_name}")
            return True

        except Exception as e:
            logger.error(f"Backup verification failed: {str(e)}")
            return False

    def _get_vm_config(self, domain_name: str) -> Dict:
        """Get VM configuration from config file."""
        for env in ['production', 'staging']:
            for vm in self.config['virtual_machines'].get(env, []):
                if vm['name'] == domain_name:
                    return vm
        return None

    def _get_memory_path(self, domain_name: str, snapshot_name: str) -> str:
        """Get path for memory state file."""
        return os.path.join(self.config['storage']['local']['path'], 
                          domain_name, snapshot_name, 'memory.state')

    def _get_disk_snapshot_path(self, disk_path: str, snapshot_name: str) -> str:
        """Get path for disk snapshot file."""
        disk_name = os.path.basename(disk_path)
        return os.path.join(self.config['storage']['local']['path'],
                          snapshot_name, f"{disk_name}.snapshot")

    def _copy_to_remote(self, source: str, dest_dir: str):
        """Copy file to remote storage."""
        if self.config['storage']['remote']['type'] == 'nfs':
            subprocess.run(['cp', '-a', source, dest_dir], check=True)
        else:
            # Add other remote storage types here
            raise NotImplementedError(f"Remote storage type {self.config['storage']['remote']['type']} not implemented")

    def _create_test_vm_xml(self, domain_name: str, snapshot_name: str) -> str:
        """Create XML for test VM."""
        vm_config = self._get_vm_config(domain_name)
        
        xml = f"""
        <domain type='kvm'>
            <name>test-{domain_name}-{snapshot_name}</name>
            <memory unit='GiB'>{vm_config['memory']}</memory>
            <vcpu>{vm_config['vcpus']}</vcpu>
            <os>
                <type arch='x86_64'>hvm</type>
            </os>
            <devices>
        """
        
        # Add disks
        for disk in vm_config['disks']:
            if disk['backup']:
                snapshot_path = self._get_disk_snapshot_path(disk['path'], snapshot_name)
                xml += f"""
                <disk type='file' device='disk'>
                    <source file='{snapshot_path}'/>
                    <target dev='vda' bus='virtio'/>
                </disk>
                """

        xml += """
            </devices>
        </domain>
        """
        
        return xml

@click.group()
def cli():
    """KVM Backup Management CLI"""
    pass

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--domain', required=True, help='Domain name')
@click.option('--snapshot-name', help='Snapshot name (optional)')
def create_backup(config, domain, snapshot_name):
    """Create backup for a KVM domain."""
    manager = KVMBackupManager(config)
    snapshot = manager.create_snapshot(domain, snapshot_name)
    click.echo(f"Created snapshot: {snapshot}")
    
    manager.backup_to_remote(domain, snapshot)
    click.echo("Backup copied to remote storage")

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--domain', required=True, help='Domain name')
@click.option('--snapshot-name', required=True, help='Snapshot name')
def restore(config, domain, snapshot_name):
    """Restore a domain from snapshot."""
    manager = KVMBackupManager(config)
    manager.restore_snapshot(domain, snapshot_name)
    click.echo(f"Restored {domain} from snapshot {snapshot_name}")

@cli.command()
@click.option('--config', '-c', required=True, help='Path to config file')
@click.option('--domain', required=True, help='Domain name')
@click.option('--snapshot-name', required=True, help='Snapshot name')
def verify(config, domain, snapshot_name):
    """Verify backup integrity."""
    manager = KVMBackupManager(config)
    success = manager.verify_backup(domain, snapshot_name)
    if success:
        click.echo("Backup verification successful")
    else:
        click.echo("Backup verification failed")
        sys.exit(1)

if __name__ == '__main__':
    cli()

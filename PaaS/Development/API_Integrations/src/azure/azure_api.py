#!/usr/bin/env python3

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import yaml

class AzureIntegration:
    def __init__(self, config_path='config/credentials.yaml'):
        """Initialize Azure API connection"""
        with open(config_path) as f:
            config = yaml.safe_load(f)['azure']
        
        self.subscription_id = config['subscription_id']
        self.credentials = ClientSecretCredential(
            tenant_id=config['tenant_id'],
            client_id=config['client_id'],
            client_secret=config['client_secret']
        )
        
        self.compute_client = ComputeManagementClient(
            self.credentials, 
            self.subscription_id
        )
        self.network_client = NetworkManagementClient(
            self.credentials, 
            self.subscription_id
        )
        self.resource_client = ResourceManagementClient(
            self.credentials, 
            self.subscription_id
        )

    def list_virtual_machines(self, resource_group):
        """List all virtual machines in a resource group"""
        return self.compute_client.virtual_machines.list(resource_group)

    def create_vm(self, resource_group, vm_name, location, vm_size, image_reference):
        """Create a new virtual machine"""
        # Create VM parameters
        vm_parameters = {
            "location": location,
            "hardware_profile": {
                "vm_size": vm_size
            },
            "storage_profile": {
                "image_reference": image_reference
            },
            "network_profile": {
                "network_interfaces": []
            }
        }
        
        return self.compute_client.virtual_machines.begin_create_or_update(
            resource_group,
            vm_name,
            vm_parameters
        )

    def start_vm(self, resource_group, vm_name):
        """Start a virtual machine"""
        return self.compute_client.virtual_machines.begin_start(
            resource_group,
            vm_name
        )

    def stop_vm(self, resource_group, vm_name):
        """Stop a virtual machine"""
        return self.compute_client.virtual_machines.begin_deallocate(
            resource_group,
            vm_name
        )

    def delete_vm(self, resource_group, vm_name):
        """Delete a virtual machine"""
        return self.compute_client.virtual_machines.begin_delete(
            resource_group,
            vm_name
        )

    def get_vm_status(self, resource_group, vm_name):
        """Get the status of a virtual machine"""
        return self.compute_client.virtual_machines.instance_view(
            resource_group,
            vm_name
        )

    def list_resource_groups(self):
        """List all resource groups"""
        return self.resource_client.resource_groups.list()

    def create_resource_group(self, name, location):
        """Create a new resource group"""
        parameters = {"location": location}
        return self.resource_client.resource_groups.create_or_update(
            name,
            parameters
        )

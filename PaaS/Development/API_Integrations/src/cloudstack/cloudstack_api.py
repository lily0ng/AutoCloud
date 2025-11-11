#!/usr/bin/env python3

import os
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeSize, NodeImage, NodeLocation
import yaml

class CloudStackIntegration:
    def __init__(self, config_path='config/credentials.yaml'):
        """Initialize CloudStack API connection"""
        with open(config_path) as f:
            config = yaml.safe_load(f)['cloudstack']
        
        self.cls = get_driver(Provider.CLOUDSTACK)
        self.driver = self.cls(
            key=config['api_key'],
            secret=config['secret_key'],
            host=config['host'],
            path=config.get('path', '/client/api'),
            secure=config.get('secure', True)
        )

    def list_virtual_machines(self):
        """List all virtual machines"""
        return self.driver.list_nodes()

    def create_kvm_instance(self, name, size, image, location=None):
        """Create a new KVM instance"""
        return self.driver.create_node(
            name=name,
            size=size,
            image=image,
            location=location,
            ex_hypervisor='KVM'
        )

    def get_instance_status(self, instance_id):
        """Get status of a specific instance"""
        nodes = self.driver.list_nodes()
        for node in nodes:
            if node.id == instance_id:
                return node.state
        return None

    def stop_instance(self, instance_id):
        """Stop a running instance"""
        nodes = self.driver.list_nodes()
        for node in nodes:
            if node.id == instance_id:
                return self.driver.ex_stop_node(node)
        return False

    def start_instance(self, instance_id):
        """Start a stopped instance"""
        nodes = self.driver.list_nodes()
        for node in nodes:
            if node.id == instance_id:
                return self.driver.ex_start_node(node)
        return False

    def delete_instance(self, instance_id):
        """Delete an instance"""
        nodes = self.driver.list_nodes()
        for node in nodes:
            if node.id == instance_id:
                return self.driver.destroy_node(node)
        return False

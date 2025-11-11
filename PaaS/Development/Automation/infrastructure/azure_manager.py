from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import DefaultAzureCredential
from typing import Dict, Any
import logging

class AzureManager:
    def __init__(self, subscription_id: str):
        self.credential = DefaultAzureCredential()
        self.subscription_id = subscription_id
        self.compute_client = ComputeManagementClient(self.credential, subscription_id)
        self.network_client = NetworkManagementClient(self.credential, subscription_id)
        self.resource_client = ResourceManagementClient(self.credential, subscription_id)
        self.logger = logging.getLogger(__name__)

    def create_resource_group(
        self,
        resource_group_name: str,
        location: str = "eastus"
    ) -> Dict[str, Any]:
        try:
            return self.resource_client.resource_groups.create_or_update(
                resource_group_name,
                {"location": location}
            )
        except Exception as e:
            self.logger.error(f"Failed to create resource group: {str(e)}")
            raise

    def create_virtual_network(
        self,
        resource_group_name: str,
        vnet_name: str,
        location: str = "eastus"
    ) -> Dict[str, Any]:
        try:
            return self.network_client.virtual_networks.begin_create_or_update(
                resource_group_name,
                vnet_name,
                {
                    "location": location,
                    "address_space": {
                        "address_prefixes": ["10.0.0.0/16"]
                    }
                }
            ).result()
        except Exception as e:
            self.logger.error(f"Failed to create virtual network: {str(e)}")
            raise

    def create_aks_cluster(
        self,
        resource_group_name: str,
        cluster_name: str,
        location: str = "eastus"
    ) -> Dict[str, Any]:
        try:
            return self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
                resource_group_name,
                cluster_name,
                {
                    "location": location,
                    "sku": {
                        "name": "Standard_DS1_v2",
                        "tier": "Standard",
                        "capacity": 1
                    },
                    "orchestration_mode": "Uniform"
                }
            ).result()
        except Exception as e:
            self.logger.error(f"Failed to create AKS cluster: {str(e)}")
            raise

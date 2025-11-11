from google.cloud import compute_v1
from google.cloud import container_v1
from google.cloud import storage
from typing import Dict, Any
import logging

class GCPManager:
    def __init__(self, project_id: str, zone: str = "us-central1-a"):
        self.project_id = project_id
        self.zone = zone
        self.compute_client = compute_v1.InstancesClient()
        self.gke_client = container_v1.ClusterManagerClient()
        self.storage_client = storage.Client()
        self.logger = logging.getLogger(__name__)

    def create_vpc_network(self, network_name: str) -> Dict[str, Any]:
        try:
            network_client = compute_v1.NetworksClient()
            network = {
                "name": network_name,
                "auto_create_subnetworks": True
            }
            operation = network_client.insert(
                project=self.project_id,
                network_resource=network
            )
            return operation.result()
        except Exception as e:
            self.logger.error(f"Failed to create VPC network: {str(e)}")
            raise

    def create_gke_cluster(
        self,
        cluster_name: str,
        node_count: int = 3
    ) -> Dict[str, Any]:
        try:
            cluster_location = f"projects/{self.project_id}/locations/{self.zone}"
            cluster = {
                "name": cluster_name,
                "initial_node_count": node_count,
                "node_config": {
                    "machine_type": "e2-medium",
                    "disk_size_gb": 100,
                    "oauth_scopes": [
                        "https://www.googleapis.com/auth/devstorage.read_only",
                        "https://www.googleapis.com/auth/logging.write",
                        "https://www.googleapis.com/auth/monitoring",
                        "https://www.googleapis.com/auth/servicecontrol",
                        "https://www.googleapis.com/auth/service.management.readonly",
                        "https://www.googleapis.com/auth/trace.append"
                    ]
                }
            }
            request = {"parent": cluster_location, "cluster": cluster}
            operation = self.gke_client.create_cluster(request=request)
            return operation.result()
        except Exception as e:
            self.logger.error(f"Failed to create GKE cluster: {str(e)}")
            raise

    def create_cloud_storage_bucket(
        self,
        bucket_name: str,
        location: str = "US"
    ) -> Dict[str, Any]:
        try:
            bucket = self.storage_client.create_bucket(
                bucket_name,
                location=location
            )
            return {"name": bucket.name, "location": bucket.location}
        except Exception as e:
            self.logger.error(f"Failed to create storage bucket: {str(e)}")
            raise

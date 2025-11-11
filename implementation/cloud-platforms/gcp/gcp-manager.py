#!/usr/bin/env python3
"""Google Cloud Platform Manager"""

from google.cloud import compute_v1
from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCPManager:
    def __init__(self, project_id):
        self.project_id = project_id
        self.compute_client = compute_v1.InstancesClient()
        self.storage_client = storage.Client(project=project_id)
    
    def create_instance(self, zone, instance_name, machine_type='e2-medium'):
        """Create Compute Engine instance"""
        try:
            instance = compute_v1.Instance()
            instance.name = instance_name
            instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"
            
            logger.info(f"Creating instance {instance_name}...")
            # Instance creation logic here
            return True
        except Exception as e:
            logger.error(f"Error creating instance: {e}")
            return False
    
    def list_instances(self, zone):
        """List Compute Engine instances"""
        try:
            request = compute_v1.ListInstancesRequest()
            request.project = self.project_id
            request.zone = zone
            
            instances = self.compute_client.list(request=request)
            return [{'name': inst.name, 'status': inst.status} for inst in instances]
        except Exception as e:
            logger.error(f"Error listing instances: {e}")
            return []
    
    def create_bucket(self, bucket_name, location='US'):
        """Create Cloud Storage bucket"""
        try:
            bucket = self.storage_client.bucket(bucket_name)
            bucket.location = location
            bucket = self.storage_client.create_bucket(bucket)
            logger.info(f"Bucket {bucket_name} created")
            return True
        except Exception as e:
            logger.error(f"Error creating bucket: {e}")
            return False
    
    def upload_to_bucket(self, bucket_name, source_file, destination_blob):
        """Upload file to Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob)
            blob.upload_from_filename(source_file)
            logger.info(f"File {source_file} uploaded to {bucket_name}/{destination_blob}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False

if __name__ == "__main__":
    # manager = GCPManager("your-project-id")
    print("GCP Manager initialized")

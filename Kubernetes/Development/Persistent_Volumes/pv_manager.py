#!/usr/bin/env python3

from kubernetes import client, config
import yaml
import os
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PVManager:
    def __init__(self):
        try:
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            logger.info("Successfully initialized Kubernetes client")
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise

    def create_pv_from_yaml(self, yaml_file: str) -> None:
        """Create a PV from a YAML file"""
        try:
            with open(yaml_file, 'r') as f:
                pv_config = yaml.safe_load_all(f)
                for config_item in pv_config:
                    if config_item["kind"] == "PersistentVolume":
                        self.v1.create_persistent_volume(body=config_item)
                        logger.info(f"Created PV: {config_item['metadata']['name']}")
                    elif config_item["kind"] == "PersistentVolumeClaim":
                        self.v1.create_namespaced_persistent_volume_claim(
                            namespace="default",
                            body=config_item
                        )
                        logger.info(f"Created PVC: {config_item['metadata']['name']}")
        except Exception as e:
            logger.error(f"Failed to create PV from YAML: {e}")
            raise

    def list_pvs(self) -> List[Dict]:
        """List all PVs in the cluster"""
        try:
            pvs = self.v1.list_persistent_volume()
            return [{
                'name': pv.metadata.name,
                'capacity': pv.spec.capacity['storage'],
                'status': pv.status.phase,
                'storage_class': pv.spec.storage_class_name
            } for pv in pvs.items]
        except Exception as e:
            logger.error(f"Failed to list PVs: {e}")
            raise

    def list_pvcs(self) -> List[Dict]:
        """List all PVCs in the cluster"""
        try:
            pvcs = self.v1.list_persistent_volume_claim_for_all_namespaces()
            return [{
                'name': pvc.metadata.name,
                'namespace': pvc.metadata.namespace,
                'status': pvc.status.phase,
                'volume': pvc.spec.volume_name if pvc.spec.volume_name else 'Not Bound'
            } for pvc in pvcs.items]
        except Exception as e:
            logger.error(f"Failed to list PVCs: {e}")
            raise

    def delete_pv(self, name: str) -> None:
        """Delete a PV by name"""
        try:
            self.v1.delete_persistent_volume(name)
            logger.info(f"Deleted PV: {name}")
        except Exception as e:
            logger.error(f"Failed to delete PV {name}: {e}")
            raise

    def get_pv_status(self, name: str) -> Dict:
        """Get detailed status of a PV"""
        try:
            pv = self.v1.read_persistent_volume(name)
            return {
                'name': pv.metadata.name,
                'status': pv.status.phase,
                'capacity': pv.spec.capacity['storage'],
                'access_modes': pv.spec.access_modes,
                'storage_class': pv.spec.storage_class_name,
                'reclaim_policy': pv.spec.persistent_volume_reclaim_policy
            }
        except Exception as e:
            logger.error(f"Failed to get PV status for {name}: {e}")
            raise

def main():
    pv_manager = PVManager()
    
    while True:
        print("\nKubernetes PV Manager")
        print("1. Create PV from YAML")
        print("2. List PVs")
        print("3. List PVCs")
        print("4. Delete PV")
        print("5. Get PV Status")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        try:
            if choice == '1':
                yaml_file = input("Enter YAML file path: ")
                pv_manager.create_pv_from_yaml(yaml_file)
            
            elif choice == '2':
                pvs = pv_manager.list_pvs()
                for pv in pvs:
                    print(f"\nName: {pv['name']}")
                    print(f"Capacity: {pv['capacity']}")
                    print(f"Status: {pv['status']}")
                    print(f"Storage Class: {pv['storage_class']}")
            
            elif choice == '3':
                pvcs = pv_manager.list_pvcs()
                for pvc in pvcs:
                    print(f"\nName: {pvc['name']}")
                    print(f"Namespace: {pvc['namespace']}")
                    print(f"Status: {pvc['status']}")
                    print(f"Volume: {pvc['volume']}")
            
            elif choice == '4':
                name = input("Enter PV name to delete: ")
                pv_manager.delete_pv(name)
            
            elif choice == '5':
                name = input("Enter PV name: ")
                status = pv_manager.get_pv_status(name)
                print("\nPV Status:")
                for key, value in status.items():
                    print(f"{key}: {value}")
            
            elif choice == '6':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice!")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

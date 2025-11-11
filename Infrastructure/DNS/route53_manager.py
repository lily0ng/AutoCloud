"""
Route53 DNS management
"""
import boto3
from typing import List, Dict


class Route53Manager:
    """Manage Route53 hosted zones and records"""
    
    def __init__(self):
        self.route53_client = boto3.client('route53')
    
    def create_hosted_zone(self, domain_name: str, comment: str = ""):
        """Create hosted zone"""
        try:
            import time
            response = self.route53_client.create_hosted_zone(
                Name=domain_name,
                CallerReference=str(int(time.time())),
                HostedZoneConfig={'Comment': comment, 'PrivateZone': False}
            )
            return response['HostedZone']['Id']
        except Exception as e:
            raise Exception(f"Failed to create hosted zone: {str(e)}")
    
    def create_record(self, hosted_zone_id: str, record_name: str,
                     record_type: str, value: str, ttl: int = 300):
        """Create DNS record"""
        try:
            self.route53_client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': ttl,
                            'ResourceRecords': [{'Value': value}]
                        }
                    }]
                }
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create record: {str(e)}")
    
    def create_alias_record(self, hosted_zone_id: str, record_name: str,
                           target_dns: str, target_zone_id: str):
        """Create alias record"""
        try:
            self.route53_client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': target_zone_id,
                                'DNSName': target_dns,
                                'EvaluateTargetHealth': True
                            }
                        }
                    }]
                }
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create alias record: {str(e)}")
    
    def list_hosted_zones(self):
        """List all hosted zones"""
        try:
            response = self.route53_client.list_hosted_zones()
            return response['HostedZones']
        except Exception as e:
            raise Exception(f"Failed to list hosted zones: {str(e)}")

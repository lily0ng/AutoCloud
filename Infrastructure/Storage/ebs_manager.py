"""
EBS volume management
"""
import boto3


class EBSManager:
    """Manage EBS volumes"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.region = region
    
    def create_volume(self, size: int, az: str, volume_type: str = 'gp3',
                     iops: int = None, encrypted: bool = True):
        """Create EBS volume"""
        try:
            params = {
                'Size': size,
                'AvailabilityZone': az,
                'VolumeType': volume_type,
                'Encrypted': encrypted
            }
            
            if iops and volume_type in ['io1', 'io2', 'gp3']:
                params['Iops'] = iops
            
            response = self.ec2_client.create_volume(**params)
            return response['VolumeId']
        except Exception as e:
            raise Exception(f"Failed to create volume: {str(e)}")
    
    def attach_volume(self, volume_id: str, instance_id: str, device: str = '/dev/sdf'):
        """Attach volume to instance"""
        try:
            self.ec2_client.attach_volume(
                VolumeId=volume_id,
                InstanceId=instance_id,
                Device=device
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to attach volume: {str(e)}")
    
    def create_snapshot(self, volume_id: str, description: str = ""):
        """Create volume snapshot"""
        try:
            response = self.ec2_client.create_snapshot(
                VolumeId=volume_id,
                Description=description
            )
            return response['SnapshotId']
        except Exception as e:
            raise Exception(f"Failed to create snapshot: {str(e)}")
    
    def delete_volume(self, volume_id: str):
        """Delete EBS volume"""
        try:
            self.ec2_client.delete_volume(VolumeId=volume_id)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete volume: {str(e)}")

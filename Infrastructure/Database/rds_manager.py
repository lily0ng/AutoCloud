"""
RDS database management
"""
import boto3


class RDSManager:
    """Manage RDS databases"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.rds_client = boto3.client('rds', region_name=region)
        self.region = region
    
    def create_db_instance(self, db_identifier: str, db_name: str, engine: str,
                          instance_class: str, username: str, password: str,
                          allocated_storage: int = 20, multi_az: bool = False):
        """Create RDS instance"""
        try:
            response = self.rds_client.create_db_instance(
                DBInstanceIdentifier=db_identifier,
                DBName=db_name,
                Engine=engine,
                DBInstanceClass=instance_class,
                MasterUsername=username,
                MasterUserPassword=password,
                AllocatedStorage=allocated_storage,
                StorageType='gp3',
                StorageEncrypted=True,
                MultiAZ=multi_az,
                BackupRetentionPeriod=7,
                PreferredBackupWindow='03:00-04:00',
                PreferredMaintenanceWindow='mon:04:00-mon:05:00',
                EnableCloudwatchLogsExports=['error', 'general', 'slowquery'],
                DeletionProtection=True
            )
            return response['DBInstance']['DBInstanceIdentifier']
        except Exception as e:
            raise Exception(f"Failed to create DB instance: {str(e)}")
    
    def create_snapshot(self, db_identifier: str, snapshot_identifier: str):
        """Create DB snapshot"""
        try:
            response = self.rds_client.create_db_snapshot(
                DBSnapshotIdentifier=snapshot_identifier,
                DBInstanceIdentifier=db_identifier
            )
            return response['DBSnapshot']['DBSnapshotIdentifier']
        except Exception as e:
            raise Exception(f"Failed to create snapshot: {str(e)}")
    
    def restore_from_snapshot(self, snapshot_id: str, new_db_identifier: str):
        """Restore DB from snapshot"""
        try:
            response = self.rds_client.restore_db_instance_from_db_snapshot(
                DBInstanceIdentifier=new_db_identifier,
                DBSnapshotIdentifier=snapshot_id
            )
            return response['DBInstance']['DBInstanceIdentifier']
        except Exception as e:
            raise Exception(f"Failed to restore from snapshot: {str(e)}")

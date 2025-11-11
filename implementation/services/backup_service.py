"""
Backup service for data protection
"""
import boto3
import os
import tarfile
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BackupService:
    """Handle backup operations"""
    
    def __init__(self, s3_bucket: str, aws_region: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=aws_region)
        self.bucket = s3_bucket
    
    def create_backup(self, source_path: str, backup_name: str = None):
        """Create backup archive"""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.tar.gz"
        
        try:
            with tarfile.open(backup_name, 'w:gz') as tar:
                tar.add(source_path, arcname=os.path.basename(source_path))
            
            logger.info(f"Backup created: {backup_name}")
            return backup_name
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    def upload_to_s3(self, file_path: str, s3_key: str = None):
        """Upload backup to S3"""
        if s3_key is None:
            s3_key = os.path.basename(file_path)
        
        try:
            self.s3_client.upload_file(file_path, self.bucket, s3_key)
            logger.info(f"Backup uploaded to S3: s3://{self.bucket}/{s3_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload to S3: {str(e)}")
            return False
    
    def restore_from_s3(self, s3_key: str, destination_path: str):
        """Restore backup from S3"""
        try:
            self.s3_client.download_file(self.bucket, s3_key, destination_path)
            logger.info(f"Backup restored from S3: {s3_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore from S3: {str(e)}")
            return False
    
    def list_backups(self, prefix: str = ''):
        """List available backups in S3"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            
            backups = []
            for obj in response.get('Contents', []):
                backups.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified']
                })
            
            return backups
        except Exception as e:
            logger.error(f"Failed to list backups: {str(e)}")
            return []

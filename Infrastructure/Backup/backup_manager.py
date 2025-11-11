"""
AWS Backup management
"""
import boto3


class BackupManager:
    """Manage AWS Backup plans and vaults"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.backup_client = boto3.client('backup', region_name=region)
        self.region = region
    
    def create_backup_vault(self, vault_name: str):
        """Create backup vault"""
        try:
            response = self.backup_client.create_backup_vault(BackupVaultName=vault_name)
            return response['BackupVaultArn']
        except Exception as e:
            raise Exception(f"Failed to create backup vault: {str(e)}")
    
    def create_backup_plan(self, plan_name: str, vault_name: str,
                          schedule: str = 'cron(0 5 ? * * *)',
                          retention_days: int = 30):
        """Create backup plan"""
        try:
            backup_plan = {
                'BackupPlanName': plan_name,
                'Rules': [{
                    'RuleName': f'{plan_name}-rule',
                    'TargetBackupVaultName': vault_name,
                    'ScheduleExpression': schedule,
                    'StartWindowMinutes': 60,
                    'CompletionWindowMinutes': 120,
                    'Lifecycle': {
                        'DeleteAfterDays': retention_days
                    }
                }]
            }
            
            response = self.backup_client.create_backup_plan(BackupPlan=backup_plan)
            return response['BackupPlanId']
        except Exception as e:
            raise Exception(f"Failed to create backup plan: {str(e)}")
    
    def create_backup_selection(self, plan_id: str, selection_name: str,
                               iam_role_arn: str, resource_arns: list):
        """Create backup selection"""
        try:
            selection = {
                'SelectionName': selection_name,
                'IamRoleArn': iam_role_arn,
                'Resources': resource_arns
            }
            
            response = self.backup_client.create_backup_selection(
                BackupPlanId=plan_id,
                BackupSelection=selection
            )
            return response['SelectionId']
        except Exception as e:
            raise Exception(f"Failed to create backup selection: {str(e)}")

"""
CloudWatch monitoring and alarms
"""
import boto3
from typing import List, Dict


class CloudWatchManager:
    """Manage CloudWatch metrics and alarms"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.cw_client = boto3.client('cloudwatch', region_name=region)
        self.logs_client = boto3.client('logs', region_name=region)
        self.region = region
    
    def create_alarm(self, alarm_name: str, metric_name: str, namespace: str,
                    threshold: float, comparison: str = 'GreaterThanThreshold',
                    evaluation_periods: int = 2, period: int = 300):
        """Create CloudWatch alarm"""
        try:
            self.cw_client.put_metric_alarm(
                AlarmName=alarm_name,
                MetricName=metric_name,
                Namespace=namespace,
                Statistic='Average',
                Period=period,
                EvaluationPeriods=evaluation_periods,
                Threshold=threshold,
                ComparisonOperator=comparison,
                TreatMissingData='notBreaching'
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create alarm: {str(e)}")
    
    def create_log_group(self, log_group_name: str, retention_days: int = 7):
        """Create CloudWatch log group"""
        try:
            self.logs_client.create_log_group(logGroupName=log_group_name)
            self.logs_client.put_retention_policy(
                logGroupName=log_group_name,
                retentionInDays=retention_days
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create log group: {str(e)}")
    
    def put_metric_data(self, namespace: str, metric_name: str, value: float,
                       dimensions: List[Dict] = None):
        """Put custom metric data"""
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'None'
            }
            
            if dimensions:
                metric_data['Dimensions'] = dimensions
            
            self.cw_client.put_metric_data(
                Namespace=namespace,
                MetricData=[metric_data]
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to put metric data: {str(e)}")

"""
AWS cost optimization utilities
"""
import boto3
from datetime import datetime, timedelta


class CostOptimizer:
    """Analyze and optimize AWS costs"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ce_client = boto3.client('ce', region_name='us-east-1')  # Cost Explorer is us-east-1 only
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.region = region
    
    def get_cost_and_usage(self, start_date: str, end_date: str, granularity: str = 'DAILY'):
        """Get cost and usage data"""
        try:
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity=granularity,
                Metrics=['UnblendedCost', 'UsageQuantity'],
                GroupBy=[{'Type': 'SERVICE', 'Key': 'SERVICE'}]
            )
            return response['ResultsByTime']
        except Exception as e:
            raise Exception(f"Failed to get cost data: {str(e)}")
    
    def find_idle_resources(self):
        """Find idle EC2 instances"""
        try:
            idle_instances = []
            
            # Get CloudWatch metrics for CPU utilization
            cw_client = boto3.client('cloudwatch', region_name=self.region)
            ec2_response = self.ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            for reservation in ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    
                    # Check CPU utilization for last 7 days
                    end_time = datetime.utcnow()
                    start_time = end_time - timedelta(days=7)
                    
                    metrics = cw_client.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                        StartTime=start_time,
                        EndTime=end_time,
                        Period=86400,
                        Statistics=['Average']
                    )
                    
                    if metrics['Datapoints']:
                        avg_cpu = sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints'])
                        if avg_cpu < 5:  # Less than 5% CPU
                            idle_instances.append({
                                'instance_id': instance_id,
                                'instance_type': instance['InstanceType'],
                                'avg_cpu': avg_cpu
                            })
            
            return idle_instances
        except Exception as e:
            raise Exception(f"Failed to find idle resources: {str(e)}")
    
    def get_savings_recommendations(self):
        """Get cost savings recommendations"""
        try:
            response = self.ce_client.get_rightsizing_recommendation(
                Service='AmazonEC2',
                Configuration={'RecommendationTarget': 'SAME_INSTANCE_FAMILY'}
            )
            return response.get('RightsizingRecommendations', [])
        except Exception as e:
            raise Exception(f"Failed to get recommendations: {str(e)}")

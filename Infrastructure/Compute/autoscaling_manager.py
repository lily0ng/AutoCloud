"""
Auto Scaling group management
"""
import boto3
from typing import List


class AutoScalingManager:
    """Manage Auto Scaling groups"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.asg_client = boto3.client('autoscaling', region_name=region)
        self.region = region
    
    def create_auto_scaling_group(self, name: str, launch_template_id: str,
                                  min_size: int, max_size: int, desired_size: int,
                                  subnet_ids: List[str], target_group_arns: List[str] = None):
        """Create Auto Scaling group"""
        try:
            config = {
                'AutoScalingGroupName': name,
                'LaunchTemplate': {'LaunchTemplateId': launch_template_id, 'Version': '$Latest'},
                'MinSize': min_size,
                'MaxSize': max_size,
                'DesiredCapacity': desired_size,
                'VPCZoneIdentifier': ','.join(subnet_ids),
                'HealthCheckType': 'ELB',
                'HealthCheckGracePeriod': 300
            }
            
            if target_group_arns:
                config['TargetGroupARNs'] = target_group_arns
            
            self.asg_client.create_auto_scaling_group(**config)
            return True
        except Exception as e:
            raise Exception(f"Failed to create ASG: {str(e)}")
    
    def create_scaling_policy(self, asg_name: str, policy_name: str,
                             target_value: float, metric_type: str = 'ASGAverageCPUUtilization'):
        """Create target tracking scaling policy"""
        try:
            response = self.asg_client.put_scaling_policy(
                AutoScalingGroupName=asg_name,
                PolicyName=policy_name,
                PolicyType='TargetTrackingScaling',
                TargetTrackingConfiguration={
                    'PredefinedMetricSpecification': {
                        'PredefinedMetricType': metric_type
                    },
                    'TargetValue': target_value
                }
            )
            return response['PolicyARN']
        except Exception as e:
            raise Exception(f"Failed to create scaling policy: {str(e)}")

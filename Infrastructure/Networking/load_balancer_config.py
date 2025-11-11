"""
Load balancer configuration manager
"""
from typing import List, Dict
import boto3


class LoadBalancerConfig:
    """Manage load balancer configurations"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.elb_client = boto3.client('elbv2', region_name=region)
        self.region = region
    
    def create_alb(self, name: str, subnets: List[str], security_groups: List[str],
                   scheme: str = 'internet-facing', tags: List[Dict] = None):
        """Create Application Load Balancer"""
        try:
            response = self.elb_client.create_load_balancer(
                Name=name,
                Subnets=subnets,
                SecurityGroups=security_groups,
                Scheme=scheme,
                Type='application',
                IpAddressType='ipv4',
                Tags=tags or []
            )
            return response['LoadBalancers'][0]
        except Exception as e:
            raise Exception(f"Failed to create ALB: {str(e)}")
    
    def create_target_group(self, name: str, vpc_id: str, port: int = 80,
                           protocol: str = 'HTTP', health_check: Dict = None):
        """Create target group"""
        try:
            health_check = health_check or {
                'Enabled': True,
                'HealthCheckPath': '/health',
                'HealthCheckIntervalSeconds': 30,
                'HealthCheckTimeoutSeconds': 5,
                'HealthyThresholdCount': 2,
                'UnhealthyThresholdCount': 2
            }
            
            response = self.elb_client.create_target_group(
                Name=name,
                Protocol=protocol,
                Port=port,
                VpcId=vpc_id,
                TargetType='ip',
                HealthCheckEnabled=health_check['Enabled'],
                HealthCheckPath=health_check['HealthCheckPath'],
                HealthCheckIntervalSeconds=health_check['HealthCheckIntervalSeconds'],
                HealthCheckTimeoutSeconds=health_check['HealthCheckTimeoutSeconds'],
                HealthyThresholdCount=health_check['HealthyThresholdCount'],
                UnhealthyThresholdCount=health_check['UnhealthyThresholdCount']
            )
            return response['TargetGroups'][0]
        except Exception as e:
            raise Exception(f"Failed to create target group: {str(e)}")
    
    def create_listener(self, lb_arn: str, target_group_arn: str, 
                       port: int = 80, protocol: str = 'HTTP', 
                       certificate_arn: str = None):
        """Create listener"""
        try:
            default_actions = [{
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }]
            
            listener_config = {
                'LoadBalancerArn': lb_arn,
                'Protocol': protocol,
                'Port': port,
                'DefaultActions': default_actions
            }
            
            if protocol == 'HTTPS' and certificate_arn:
                listener_config['Certificates'] = [{'CertificateArn': certificate_arn}]
                listener_config['SslPolicy'] = 'ELBSecurityPolicy-TLS-1-2-2017-01'
            
            response = self.elb_client.create_listener(**listener_config)
            return response['Listeners'][0]
        except Exception as e:
            raise Exception(f"Failed to create listener: {str(e)}")
    
    def register_targets(self, target_group_arn: str, targets: List[Dict]):
        """Register targets with target group"""
        try:
            self.elb_client.register_targets(
                TargetGroupArn=target_group_arn,
                Targets=targets
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to register targets: {str(e)}")

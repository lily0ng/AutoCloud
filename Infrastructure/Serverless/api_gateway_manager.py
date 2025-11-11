"""
API Gateway management
"""
import boto3


class APIGatewayManager:
    """Manage API Gateway"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.apigw_client = boto3.client('apigatewayv2', region_name=region)
        self.region = region
    
    def create_http_api(self, name: str, description: str = ""):
        """Create HTTP API"""
        try:
            response = self.apigw_client.create_api(
                Name=name,
                ProtocolType='HTTP',
                Description=description,
                CorsConfiguration={
                    'AllowOrigins': ['*'],
                    'AllowMethods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                    'AllowHeaders': ['*'],
                    'MaxAge': 300
                }
            )
            return response['ApiId']
        except Exception as e:
            raise Exception(f"Failed to create HTTP API: {str(e)}")
    
    def create_integration(self, api_id: str, integration_uri: str,
                          integration_type: str = 'AWS_PROXY'):
        """Create API integration"""
        try:
            response = self.apigw_client.create_integration(
                ApiId=api_id,
                IntegrationType=integration_type,
                IntegrationUri=integration_uri,
                IntegrationMethod='POST',
                PayloadFormatVersion='2.0'
            )
            return response['IntegrationId']
        except Exception as e:
            raise Exception(f"Failed to create integration: {str(e)}")
    
    def create_route(self, api_id: str, route_key: str, integration_id: str):
        """Create API route"""
        try:
            response = self.apigw_client.create_route(
                ApiId=api_id,
                RouteKey=route_key,
                Target=f'integrations/{integration_id}'
            )
            return response['RouteId']
        except Exception as e:
            raise Exception(f"Failed to create route: {str(e)}")
    
    def create_stage(self, api_id: str, stage_name: str, auto_deploy: bool = True):
        """Create API stage"""
        try:
            response = self.apigw_client.create_stage(
                ApiId=api_id,
                StageName=stage_name,
                AutoDeploy=auto_deploy
            )
            return response['StageName']
        except Exception as e:
            raise Exception(f"Failed to create stage: {str(e)}")

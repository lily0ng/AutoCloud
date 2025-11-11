"""
ECR repository management
"""
import boto3
import base64


class ECRManager:
    """Manage ECR repositories"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.ecr_client = boto3.client('ecr', region_name=region)
        self.region = region
    
    def create_repository(self, repository_name: str, image_scanning: bool = True,
                         encryption: bool = True):
        """Create ECR repository"""
        try:
            params = {
                'repositoryName': repository_name,
                'imageScanningConfiguration': {'scanOnPush': image_scanning}
            }
            
            if encryption:
                params['encryptionConfiguration'] = {'encryptionType': 'AES256'}
            
            response = self.ecr_client.create_repository(**params)
            return response['repository']['repositoryUri']
        except Exception as e:
            raise Exception(f"Failed to create repository: {str(e)}")
    
    def set_lifecycle_policy(self, repository_name: str, max_image_count: int = 30):
        """Set lifecycle policy for repository"""
        try:
            policy = {
                'rules': [
                    {
                        'rulePriority': 1,
                        'description': f'Keep last {max_image_count} images',
                        'selection': {
                            'tagStatus': 'any',
                            'countType': 'imageCountMoreThan',
                            'countNumber': max_image_count
                        },
                        'action': {'type': 'expire'}
                    }
                ]
            }
            
            import json
            self.ecr_client.put_lifecycle_policy(
                repositoryName=repository_name,
                lifecyclePolicyText=json.dumps(policy)
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to set lifecycle policy: {str(e)}")
    
    def get_authorization_token(self):
        """Get Docker authorization token"""
        try:
            response = self.ecr_client.get_authorization_token()
            token = response['authorizationData'][0]['authorizationToken']
            endpoint = response['authorizationData'][0]['proxyEndpoint']
            
            decoded = base64.b64decode(token).decode('utf-8')
            username, password = decoded.split(':')
            
            return {
                'username': username,
                'password': password,
                'endpoint': endpoint
            }
        except Exception as e:
            raise Exception(f"Failed to get authorization token: {str(e)}")
    
    def list_images(self, repository_name: str):
        """List images in repository"""
        try:
            response = self.ecr_client.list_images(repositoryName=repository_name)
            return response['imageIds']
        except Exception as e:
            raise Exception(f"Failed to list images: {str(e)}")

"""
CloudFront CDN management
"""
import boto3
from typing import List, Dict
import time


class CloudFrontManager:
    """Manage CloudFront distributions"""
    
    def __init__(self):
        self.cf_client = boto3.client('cloudfront')
    
    def create_distribution(self, origin_domain: str, aliases: List[str] = None,
                           certificate_arn: str = None, price_class: str = 'PriceClass_100'):
        """Create CloudFront distribution"""
        try:
            caller_reference = str(int(time.time()))
            
            config = {
                'CallerReference': caller_reference,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': 'origin1',
                        'DomainName': origin_domain,
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only'
                        }
                    }]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': 'origin1',
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'AllowedMethods': {
                        'Quantity': 7,
                        'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE']
                    },
                    'ForwardedValues': {
                        'QueryString': True,
                        'Cookies': {'Forward': 'all'}
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000
                },
                'Comment': 'AutoCloud CDN Distribution',
                'Enabled': True,
                'PriceClass': price_class
            }
            
            if aliases:
                config['Aliases'] = {'Quantity': len(aliases), 'Items': aliases}
            
            if certificate_arn:
                config['ViewerCertificate'] = {
                    'ACMCertificateArn': certificate_arn,
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.2_2021'
                }
            
            response = self.cf_client.create_distribution(DistributionConfig=config)
            return response['Distribution']['Id']
        except Exception as e:
            raise Exception(f"Failed to create distribution: {str(e)}")
    
    def invalidate_cache(self, distribution_id: str, paths: List[str]):
        """Invalidate CloudFront cache"""
        try:
            self.cf_client.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={
                    'Paths': {'Quantity': len(paths), 'Items': paths},
                    'CallerReference': str(int(time.time()))
                }
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to invalidate cache: {str(e)}")

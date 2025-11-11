// CloudFront CDN Integration with S3
import { CloudFrontClient, CreateDistributionCommand } from '@aws-sdk/client-cloudfront';

interface CloudFrontConfig {
  bucketName: string;
  originAccessIdentity: string;
  priceClass?: string;
  enabled?: boolean;
}

class CloudFrontIntegration {
  private client: CloudFrontClient;

  constructor(region: string = 'us-east-1') {
    this.client = new CloudFrontClient({ region });
  }

  async createDistribution(config: CloudFrontConfig): Promise<string> {
    const command = new CreateDistributionCommand({
      DistributionConfig: {
        CallerReference: Date.now().toString(),
        Comment: `CloudFront distribution for ${config.bucketName}`,
        Enabled: config.enabled ?? true,
        Origins: {
          Quantity: 1,
          Items: [
            {
              Id: `S3-${config.bucketName}`,
              DomainName: `${config.bucketName}.s3.amazonaws.com`,
              S3OriginConfig: {
                OriginAccessIdentity: `origin-access-identity/cloudfront/${config.originAccessIdentity}`
              }
            }
          ]
        },
        DefaultCacheBehavior: {
          TargetOriginId: `S3-${config.bucketName}`,
          ViewerProtocolPolicy: 'redirect-to-https',
          AllowedMethods: {
            Quantity: 2,
            Items: ['GET', 'HEAD']
          },
          ForwardedValues: {
            QueryString: false,
            Cookies: {
              Forward: 'none'
            }
          },
          MinTTL: 0,
          TrustedSigners: {
            Enabled: false,
            Quantity: 0
          }
        },
        PriceClass: config.priceClass || 'PriceClass_100'
      }
    });

    try {
      const response = await this.client.send(command);
      const distributionId = response.Distribution?.Id;
      const domainName = response.Distribution?.DomainName;
      
      console.log(`CloudFront distribution created: ${distributionId}`);
      console.log(`Distribution URL: https://${domainName}`);
      
      return distributionId || '';
    } catch (error) {
      console.error('Error creating CloudFront distribution:', error);
      throw error;
    }
  }

  generateCDNUrl(distributionDomain: string, objectKey: string): string {
    return `https://${distributionDomain}/${objectKey}`;
  }
}

// Usage
const cloudfront = new CloudFrontIntegration();

cloudfront.createDistribution({
  bucketName: 'my-static-website',
  originAccessIdentity: 'E1234567890ABC',
  priceClass: 'PriceClass_100',
  enabled: true
});

export { CloudFrontIntegration, CloudFrontConfig };

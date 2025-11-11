// S3 Static Website Hosting Manager
import { S3Client, PutBucketWebsiteCommand, GetBucketWebsiteCommand } from '@aws-sdk/client-s3';

interface WebsiteConfig {
  indexDocument: string;
  errorDocument: string;
  redirectRules?: RedirectRule[];
}

interface RedirectRule {
  condition?: {
    httpErrorCodeReturnedEquals?: string;
    keyPrefixEquals?: string;
  };
  redirect: {
    hostName?: string;
    httpRedirectCode?: string;
    protocol?: string;
    replaceKeyPrefixWith?: string;
    replaceKeyWith?: string;
  };
}

class StaticWebsiteManager {
  private client: S3Client;

  constructor(region: string = 'us-east-1') {
    this.client = new S3Client({ region });
  }

  async enableWebsiteHosting(bucketName: string, config: WebsiteConfig): Promise<void> {
    const command = new PutBucketWebsiteCommand({
      Bucket: bucketName,
      WebsiteConfiguration: {
        IndexDocument: {
          Suffix: config.indexDocument
        },
        ErrorDocument: {
          Key: config.errorDocument
        },
        RoutingRules: config.redirectRules
      }
    });

    try {
      await this.client.send(command);
      console.log(`Website hosting enabled for bucket: ${bucketName}`);
      console.log(`Website URL: http://${bucketName}.s3-website-us-east-1.amazonaws.com`);
    } catch (error) {
      console.error('Error enabling website hosting:', error);
      throw error;
    }
  }

  async getWebsiteConfig(bucketName: string): Promise<any> {
    const command = new GetBucketWebsiteCommand({
      Bucket: bucketName
    });

    try {
      const response = await this.client.send(command);
      return response;
    } catch (error) {
      console.error('Error getting website config:', error);
      throw error;
    }
  }

  generateWebsiteURL(bucketName: string, region: string = 'us-east-1'): string {
    return `http://${bucketName}.s3-website-${region}.amazonaws.com`;
  }
}

// Usage
const manager = new StaticWebsiteManager();

manager.enableWebsiteHosting('my-static-website', {
  indexDocument: 'index.html',
  errorDocument: 'error.html',
  redirectRules: [
    {
      condition: {
        httpErrorCodeReturnedEquals: '404'
      },
      redirect: {
        replaceKeyWith: 'error.html'
      }
    }
  ]
});

export { StaticWebsiteManager, WebsiteConfig, RedirectRule };

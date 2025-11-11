// Lambda Deployment Automation
import { LambdaClient, UpdateFunctionCodeCommand, PublishVersionCommand, UpdateAliasCommand } from '@aws-sdk/client-lambda';
import * as fs from 'fs';
import * as path from 'path';

interface DeploymentConfig {
  functionName: string;
  zipFilePath: string;
  alias?: string;
  description?: string;
}

class LambdaDeployment {
  private client: LambdaClient;

  constructor(region: string = 'us-east-1') {
    this.client = new LambdaClient({ region });
  }

  async deployFunction(config: DeploymentConfig): Promise<string> {
    try {
      // Read the deployment package
      const zipBuffer = fs.readFileSync(config.zipFilePath);

      // Update function code
      console.log(`Updating function code for: ${config.functionName}`);
      const updateCommand = new UpdateFunctionCodeCommand({
        FunctionName: config.functionName,
        ZipFile: zipBuffer
      });

      await this.client.send(updateCommand);
      console.log('Function code updated successfully');

      // Publish new version
      console.log('Publishing new version...');
      const publishCommand = new PublishVersionCommand({
        FunctionName: config.functionName,
        Description: config.description || `Deployed at ${new Date().toISOString()}`
      });

      const publishResult = await this.client.send(publishCommand);
      const version = publishResult.Version || '1';
      console.log(`Published version: ${version}`);

      // Update alias if specified
      if (config.alias) {
        console.log(`Updating alias: ${config.alias}`);
        const aliasCommand = new UpdateAliasCommand({
          FunctionName: config.functionName,
          Name: config.alias,
          FunctionVersion: version
        });

        await this.client.send(aliasCommand);
        console.log(`Alias ${config.alias} updated to version ${version}`);
      }

      return version;
    } catch (error) {
      console.error('Deployment failed:', error);
      throw error;
    }
  }

  async rollback(functionName: string, alias: string, previousVersion: string): Promise<void> {
    try {
      console.log(`Rolling back ${functionName}:${alias} to version ${previousVersion}`);
      
      const command = new UpdateAliasCommand({
        FunctionName: functionName,
        Name: alias,
        FunctionVersion: previousVersion
      });

      await this.client.send(command);
      console.log('Rollback completed successfully');
    } catch (error) {
      console.error('Rollback failed:', error);
      throw error;
    }
  }

  async blueGreenDeploy(functionName: string, zipFilePath: string): Promise<void> {
    try {
      // Deploy to staging alias first
      console.log('Deploying to staging...');
      const version = await this.deployFunction({
        functionName,
        zipFilePath,
        alias: 'staging',
        description: 'Blue-Green deployment - staging'
      });

      // Wait for validation (in production, add health checks here)
      console.log('Waiting for validation...');
      await new Promise(resolve => setTimeout(resolve, 5000));

      // Promote to production
      console.log('Promoting to production...');
      const prodCommand = new UpdateAliasCommand({
        FunctionName: functionName,
        Name: 'production',
        FunctionVersion: version
      });

      await this.client.send(prodCommand);
      console.log('Blue-Green deployment completed');
    } catch (error) {
      console.error('Blue-Green deployment failed:', error);
      throw error;
    }
  }
}

// Usage
const deployment = new LambdaDeployment();

deployment.deployFunction({
  functionName: 'autocloud-function',
  zipFilePath: './dist/function.zip',
  alias: 'production',
  description: 'Production deployment v1.0.0'
}).then(version => {
  console.log(`Deployment completed. Version: ${version}`);
}).catch(error => {
  console.error('Deployment error:', error);
});

export { LambdaDeployment, DeploymentConfig };

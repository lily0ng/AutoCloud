// IAM Credential Rotation Tool
import { IAMClient, CreateAccessKeyCommand, DeleteAccessKeyCommand, ListAccessKeysCommand } from '@aws-sdk/client-iam';

interface RotationResult {
  oldAccessKeyId: string;
  newAccessKeyId: string;
  newSecretAccessKey: string;
}

class CredentialRotation {
  private client: IAMClient;

  constructor(region: string = 'us-east-1') {
    this.client = new IAMClient({ region });
  }

  async rotateAccessKey(username: string): Promise<RotationResult> {
    try {
      // List existing access keys
      const listCommand = new ListAccessKeysCommand({ UserName: username });
      const listResult = await this.client.send(listCommand);
      
      if (!listResult.AccessKeyMetadata || listResult.AccessKeyMetadata.length === 0) {
        throw new Error('No access keys found for user');
      }

      const oldAccessKeyId = listResult.AccessKeyMetadata[0].AccessKeyId!;

      // Create new access key
      console.log(`Creating new access key for user: ${username}`);
      const createCommand = new CreateAccessKeyCommand({ UserName: username });
      const createResult = await this.client.send(createCommand);

      const newAccessKeyId = createResult.AccessKey!.AccessKeyId!;
      const newSecretAccessKey = createResult.AccessKey!.SecretAccessKey!;

      console.log('New access key created successfully');
      console.log('IMPORTANT: Store these credentials securely!');
      console.log(`Access Key ID: ${newAccessKeyId}`);
      console.log(`Secret Access Key: ${newSecretAccessKey}`);

      // Wait for user confirmation before deleting old key
      console.log('\nPlease update your applications with the new credentials');
      console.log('After verification, delete the old access key manually or use deleteOldKey()');

      return {
        oldAccessKeyId,
        newAccessKeyId,
        newSecretAccessKey
      };
    } catch (error) {
      console.error('Error rotating access key:', error);
      throw error;
    }
  }

  async deleteOldKey(username: string, accessKeyId: string): Promise<void> {
    try {
      const command = new DeleteAccessKeyCommand({
        UserName: username,
        AccessKeyId: accessKeyId
      });

      await this.client.send(command);
      console.log(`Successfully deleted old access key: ${accessKeyId}`);
    } catch (error) {
      console.error('Error deleting access key:', error);
      throw error;
    }
  }

  async automatedRotation(username: string, gracePeriodDays: number = 7): Promise<void> {
    console.log(`Starting automated credential rotation for: ${username}`);
    console.log(`Grace period: ${gracePeriodDays} days`);

    const result = await this.rotateAccessKey(username);

    console.log('\nRotation completed. Old key will be deleted after grace period.');
    console.log(`Old Access Key ID: ${result.oldAccessKeyId}`);
    console.log(`New Access Key ID: ${result.newAccessKeyId}`);

    // In production, schedule deletion after grace period
    setTimeout(async () => {
      console.log(`\nGrace period ended. Deleting old key: ${result.oldAccessKeyId}`);
      await this.deleteOldKey(username, result.oldAccessKeyId);
    }, gracePeriodDays * 24 * 60 * 60 * 1000);
  }
}

// Usage
const rotation = new CredentialRotation();

rotation.rotateAccessKey('autocloud-user')
  .then(result => {
    console.log('Rotation successful');
  })
  .catch(error => {
    console.error('Rotation failed:', error);
  });

export { CredentialRotation, RotationResult };

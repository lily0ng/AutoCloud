// IAM Least Privilege Checker
import { IAMClient, SimulatePrincipalPolicyCommand, GetPolicyVersionCommand } from '@aws-sdk/client-iam';

interface PermissionCheck {
  action: string;
  resource: string;
  allowed: boolean;
}

class LeastPrivilegeChecker {
  private client: IAMClient;

  constructor(region: string = 'us-east-1') {
    this.client = new IAMClient({ region });
  }

  async checkPermissions(principalArn: string, actions: string[], resources: string[]): Promise<PermissionCheck[]> {
    const command = new SimulatePrincipalPolicyCommand({
      PolicySourceArn: principalArn,
      ActionNames: actions,
      ResourceArns: resources
    });

    try {
      const response = await this.client.send(command);
      const results: PermissionCheck[] = [];

      response.EvaluationResults?.forEach(result => {
        results.push({
          action: result.EvalActionName!,
          resource: result.EvalResourceName!,
          allowed: result.EvalDecision === 'allowed'
        });
      });

      return results;
    } catch (error) {
      console.error('Error checking permissions:', error);
      throw error;
    }
  }

  async analyzeOverPermissions(principalArn: string): Promise<string[]> {
    const dangerousActions = [
      's3:*',
      'iam:*',
      'ec2:*',
      'dynamodb:*',
      '*:*'
    ];

    const overPermissions: string[] = [];

    for (const action of dangerousActions) {
      const results = await this.checkPermissions(principalArn, [action], ['*']);
      
      results.forEach(result => {
        if (result.allowed) {
          overPermissions.push(result.action);
          console.warn(`⚠️  Over-permission detected: ${result.action}`);
        }
      });
    }

    return overPermissions;
  }

  generateLeastPrivilegePolicy(allowedActions: string[], resources: string[]): string {
    const policy = {
      Version: '2012-10-17',
      Statement: [
        {
          Effect: 'Allow',
          Action: allowedActions,
          Resource: resources
        }
      ]
    };

    return JSON.stringify(policy, null, 2);
  }

  async auditPrincipal(principalArn: string): Promise<void> {
    console.log(`\nAuditing principal: ${principalArn}`);
    console.log('=' .repeat(60));

    const overPermissions = await this.analyzeOverPermissions(principalArn);

    if (overPermissions.length === 0) {
      console.log('✅ No over-permissions detected');
    } else {
      console.log(`\n❌ Found ${overPermissions.length} over-permissions:`);
      overPermissions.forEach(perm => console.log(`   - ${perm}`));
      
      console.log('\n📋 Recommendations:');
      console.log('   1. Review and restrict wildcard permissions');
      console.log('   2. Apply principle of least privilege');
      console.log('   3. Use specific actions instead of wildcards');
    }
  }
}

// Usage
const checker = new LeastPrivilegeChecker();

checker.auditPrincipal('arn:aws:iam::123456789:user/autocloud-user')
  .then(() => console.log('\nAudit completed'))
  .catch(error => console.error('Audit failed:', error));

// Generate least privilege policy
const policy = checker.generateLeastPrivilegePolicy(
  ['s3:GetObject', 's3:PutObject'],
  ['arn:aws:s3:::autocloud-bucket/*']
);

console.log('\nGenerated Least Privilege Policy:');
console.log(policy);

export { LeastPrivilegeChecker, PermissionCheck };

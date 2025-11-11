interface TagRule {
  key: string;
  required: boolean;
  allowedValues?: string[];
}

interface Resource {
  id: string;
  name: string;
  tags: Record<string, string>;
}

class TagEnforcer {
  private rules: TagRule[] = [];

  addRule(rule: TagRule): void {
    this.rules.push(rule);
  }

  validateResource(resource: Resource): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    for (const rule of this.rules) {
      if (rule.required && !resource.tags[rule.key]) {
        errors.push(`Missing required tag: ${rule.key}`);
      }

      if (resource.tags[rule.key] && rule.allowedValues) {
        if (!rule.allowedValues.includes(resource.tags[rule.key])) {
          errors.push(
            `Invalid value for tag ${rule.key}: ${resource.tags[rule.key]}. Allowed: ${rule.allowedValues.join(', ')}`
          );
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  enforceTagsOnResources(resources: Resource[]): void {
    console.log('🏷️  Enforcing tag compliance...\n');

    let compliant = 0;
    let nonCompliant = 0;

    for (const resource of resources) {
      const result = this.validateResource(resource);

      if (result.valid) {
        console.log(`✅ ${resource.name}: Compliant`);
        compliant++;
      } else {
        console.log(`❌ ${resource.name}: Non-compliant`);
        result.errors.forEach(error => console.log(`   - ${error}`));
        nonCompliant++;
      }
    }

    console.log(`\nSummary: ${compliant} compliant, ${nonCompliant} non-compliant`);
  }

  autoTag(resource: Resource, defaultTags: Record<string, string>): void {
    for (const [key, value] of Object.entries(defaultTags)) {
      if (!resource.tags[key]) {
        resource.tags[key] = value;
        console.log(`🏷️  Auto-tagged ${resource.name}: ${key}=${value}`);
      }
    }
  }
}

// Example usage
const enforcer = new TagEnforcer();

enforcer.addRule({ key: 'Environment', required: true, allowedValues: ['dev', 'staging', 'production'] });
enforcer.addRule({ key: 'Owner', required: true });
enforcer.addRule({ key: 'CostCenter', required: true });

const resources: Resource[] = [
  {
    id: 'i-123',
    name: 'web-server-1',
    tags: { Environment: 'production', Owner: 'team-a', CostCenter: 'eng-001' },
  },
  {
    id: 'i-456',
    name: 'web-server-2',
    tags: { Environment: 'dev', Owner: 'team-b' },
  },
  {
    id: 'i-789',
    name: 'web-server-3',
    tags: { Environment: 'invalid' },
  },
];

enforcer.enforceTagsOnResources(resources);

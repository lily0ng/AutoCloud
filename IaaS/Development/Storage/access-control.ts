interface AccessPolicy {resource: string; principal: string; actions: string[]}
class AccessControl {
  policies: AccessPolicy[] = [];
  addPolicy(policy: AccessPolicy) {
    this.policies.push(policy);
    console.log(`🔐 Policy added for ${policy.principal} on ${policy.resource}`);
  }
  checkAccess(principal: string, resource: string, action: string): boolean {
    return this.policies.some(p => p.principal === principal && p.resource === resource && p.actions.includes(action));
  }
}
const ac = new AccessControl();
ac.addPolicy({resource: 'bucket-1', principal: 'user-1', actions: ['read', 'write']});
console.log('Access granted:', ac.checkAccess('user-1', 'bucket-1', 'read'));

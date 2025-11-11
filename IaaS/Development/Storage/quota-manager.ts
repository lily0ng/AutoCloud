class QuotaManager {
  quotas: Map<string, number> = new Map();
  setQuota(user: string, limit: number) {
    this.quotas.set(user, limit);
    console.log(`📊 Quota set for ${user}: ${limit}GB`);
  }
  checkQuota(user: string, usage: number): boolean {
    const limit = this.quotas.get(user) || 0;
    return usage <= limit;
  }
}
const qm = new QuotaManager();
qm.setQuota('user-1', 100);
console.log('Within quota:', qm.checkQuota('user-1', 50));

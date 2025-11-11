interface CloudResource {
  id: string;
  type: string;
  name: string;
  region: string;
  tags: Record<string, string>;
  cost: number;
}

class InventoryManager {
  private resources: Map<string, CloudResource> = new Map();

  addResource(resource: CloudResource): void {
    this.resources.set(resource.id, resource);
    console.log(`✅ Added resource: ${resource.name} (${resource.type})`);
  }

  removeResource(id: string): void {
    this.resources.delete(id);
    console.log(`🗑️  Removed resource: ${id}`);
  }

  listResources(): CloudResource[] {
    return Array.from(this.resources.values());
  }

  filterByType(type: string): CloudResource[] {
    return this.listResources().filter(r => r.type === type);
  }

  filterByRegion(region: string): CloudResource[] {
    return this.listResources().filter(r => r.region === region);
  }

  filterByTag(key: string, value: string): CloudResource[] {
    return this.listResources().filter(r => r.tags[key] === value);
  }

  calculateTotalCost(): number {
    return this.listResources().reduce((sum, r) => sum + r.cost, 0);
  }

  generateReport(): void {
    console.log('\n📊 Cloud Inventory Report');
    console.log('=========================');
    
    const byType = new Map<string, number>();
    const byRegion = new Map<string, number>();
    
    this.listResources().forEach(resource => {
      byType.set(resource.type, (byType.get(resource.type) || 0) + 1);
      byRegion.set(resource.region, (byRegion.get(resource.region) || 0) + 1);
    });
    
    console.log('\nBy Type:');
    byType.forEach((count, type) => {
      console.log(`  ${type}: ${count}`);
    });
    
    console.log('\nBy Region:');
    byRegion.forEach((count, region) => {
      console.log(`  ${region}: ${count}`);
    });
    
    console.log(`\nTotal Resources: ${this.resources.size}`);
    console.log(`Total Monthly Cost: $${this.calculateTotalCost().toFixed(2)}`);
  }
}

// Example usage
const inventory = new InventoryManager();

inventory.addResource({
  id: 'i-1234567890',
  type: 'EC2',
  name: 'web-server-1',
  region: 'us-east-1',
  tags: { Environment: 'production', Team: 'backend' },
  cost: 100.50,
});

inventory.addResource({
  id: 'db-0987654321',
  type: 'RDS',
  name: 'postgres-db',
  region: 'us-east-1',
  tags: { Environment: 'production', Team: 'backend' },
  cost: 250.00,
});

inventory.generateReport();

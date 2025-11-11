// AWS EC2 Instance Type Selector
// TypeScript implementation for instance type recommendations

interface InstanceType {
  name: string;
  vcpu: number;
  memory: number;
  storage: string;
  networkPerformance: string;
  pricePerHour: number;
  useCase: string[];
}

const instanceTypes: InstanceType[] = [
  {
    name: 't3.micro',
    vcpu: 2,
    memory: 1,
    storage: 'EBS Only',
    networkPerformance: 'Up to 5 Gigabit',
    pricePerHour: 0.0104,
    useCase: ['Development', 'Testing', 'Low Traffic']
  },
  {
    name: 't3.small',
    vcpu: 2,
    memory: 2,
    storage: 'EBS Only',
    networkPerformance: 'Up to 5 Gigabit',
    pricePerHour: 0.0208,
    useCase: ['Development', 'Testing', 'Small Applications']
  },
  {
    name: 't3.medium',
    vcpu: 2,
    memory: 4,
    storage: 'EBS Only',
    networkPerformance: 'Up to 5 Gigabit',
    pricePerHour: 0.0416,
    useCase: ['Web Servers', 'Small Databases']
  },
  {
    name: 'm5.large',
    vcpu: 2,
    memory: 8,
    storage: 'EBS Only',
    networkPerformance: 'Up to 10 Gigabit',
    pricePerHour: 0.096,
    useCase: ['General Purpose', 'Application Servers']
  },
  {
    name: 'c5.xlarge',
    vcpu: 4,
    memory: 8,
    storage: 'EBS Only',
    networkPerformance: 'Up to 10 Gigabit',
    pricePerHour: 0.17,
    useCase: ['Compute Intensive', 'Batch Processing']
  },
  {
    name: 'r5.xlarge',
    vcpu: 4,
    memory: 32,
    storage: 'EBS Only',
    networkPerformance: 'Up to 10 Gigabit',
    pricePerHour: 0.252,
    useCase: ['Memory Intensive', 'Databases', 'Caching']
  }
];

class InstanceTypeSelector {
  selectByWorkload(workload: string): InstanceType[] {
    return instanceTypes.filter(type => 
      type.useCase.some(useCase => 
        useCase.toLowerCase().includes(workload.toLowerCase())
      )
    );
  }

  selectByBudget(maxPricePerHour: number): InstanceType[] {
    return instanceTypes.filter(type => type.pricePerHour <= maxPricePerHour);
  }

  selectByResources(minVCPU: number, minMemory: number): InstanceType[] {
    return instanceTypes.filter(type => 
      type.vcpu >= minVCPU && type.memory >= minMemory
    );
  }

  recommendInstance(requirements: {
    workload?: string;
    maxBudget?: number;
    minVCPU?: number;
    minMemory?: number;
  }): InstanceType | null {
    let candidates = instanceTypes;

    if (requirements.workload) {
      candidates = this.selectByWorkload(requirements.workload);
    }

    if (requirements.maxBudget) {
      candidates = candidates.filter(type => type.pricePerHour <= requirements.maxBudget);
    }

    if (requirements.minVCPU) {
      candidates = candidates.filter(type => type.vcpu >= requirements.minVCPU);
    }

    if (requirements.minMemory) {
      candidates = candidates.filter(type => type.memory >= requirements.minMemory);
    }

    return candidates.length > 0 ? candidates[0] : null;
  }

  calculateMonthlyCost(instanceType: string, hours: number = 730): number {
    const type = instanceTypes.find(t => t.name === instanceType);
    return type ? type.pricePerHour * hours : 0;
  }
}

// Usage Example
const selector = new InstanceTypeSelector();

console.log('Instance Types for Web Servers:');
console.log(selector.selectByWorkload('Web Servers'));

console.log('\nRecommended instance for requirements:');
const recommended = selector.recommendInstance({
  workload: 'Database',
  maxBudget: 0.3,
  minVCPU: 2,
  minMemory: 8
});
console.log(recommended);

export { InstanceType, InstanceTypeSelector, instanceTypes };

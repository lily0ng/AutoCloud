// AWS EC2 Cost Calculator
// Calculate and estimate EC2 costs

interface CostBreakdown {
  instanceCost: number;
  storageCost: number;
  dataTransferCost: number;
  totalMonthlyCost: number;
}

interface PricingConfig {
  instanceType: string;
  instanceCount: number;
  hoursPerMonth: number;
  storageGB: number;
  dataTransferGB: number;
  region: string;
}

class EC2CostCalculator {
  private instancePrices: Map<string, number> = new Map([
    ['t3.micro', 0.0104],
    ['t3.small', 0.0208],
    ['t3.medium', 0.0416],
    ['t3.large', 0.0832],
    ['m5.large', 0.096],
    ['m5.xlarge', 0.192],
    ['c5.large', 0.085],
    ['c5.xlarge', 0.17],
    ['r5.large', 0.126],
    ['r5.xlarge', 0.252]
  ]);

  private storagePricePerGB = 0.10; // EBS gp3
  private dataTransferPricePerGB = 0.09; // Data transfer out

  calculateCost(config: PricingConfig): CostBreakdown {
    const instancePrice = this.instancePrices.get(config.instanceType) || 0;
    
    const instanceCost = instancePrice * config.hoursPerMonth * config.instanceCount;
    const storageCost = config.storageGB * this.storagePricePerGB;
    const dataTransferCost = config.dataTransferGB * this.dataTransferPricePerGB;
    const totalMonthlyCost = instanceCost + storageCost + dataTransferCost;

    return {
      instanceCost,
      storageCost,
      dataTransferCost,
      totalMonthlyCost
    };
  }

  calculateYearlyCost(config: PricingConfig): number {
    const monthlyCost = this.calculateCost(config);
    return monthlyCost.totalMonthlyCost * 12;
  }

  compareInstanceTypes(instanceTypes: string[], config: Omit<PricingConfig, 'instanceType'>): Map<string, CostBreakdown> {
    const comparison = new Map<string, CostBreakdown>();
    
    instanceTypes.forEach(instanceType => {
      const fullConfig = { ...config, instanceType };
      comparison.set(instanceType, this.calculateCost(fullConfig));
    });

    return comparison;
  }

  calculateReservedInstanceSavings(config: PricingConfig, reservedInstanceDiscount: number = 0.30): number {
    const onDemandCost = this.calculateYearlyCost(config);
    const reservedCost = onDemandCost * (1 - reservedInstanceDiscount);
    return onDemandCost - reservedCost;
  }

  estimateAutoScalingCost(
    minInstances: number,
    maxInstances: number,
    avgInstances: number,
    config: Omit<PricingConfig, 'instanceCount'>
  ): CostBreakdown {
    const avgConfig = { ...config, instanceCount: avgInstances };
    return this.calculateCost(avgConfig);
  }

  generateCostReport(config: PricingConfig): string {
    const breakdown = this.calculateCost(config);
    const yearlyCost = this.calculateYearlyCost(config);

    return `
╔════════════════════════════════════════════╗
║        AWS EC2 Cost Estimate Report        ║
╚════════════════════════════════════════════╝

Configuration:
  Instance Type: ${config.instanceType}
  Instance Count: ${config.instanceCount}
  Hours/Month: ${config.hoursPerMonth}
  Storage: ${config.storageGB} GB
  Data Transfer: ${config.dataTransferGB} GB
  Region: ${config.region}

Monthly Cost Breakdown:
  Instance Cost:      $${breakdown.instanceCost.toFixed(2)}
  Storage Cost:       $${breakdown.storageCost.toFixed(2)}
  Data Transfer Cost: $${breakdown.dataTransferCost.toFixed(2)}
  ─────────────────────────────────────────
  Total Monthly Cost: $${breakdown.totalMonthlyCost.toFixed(2)}

Yearly Cost: $${yearlyCost.toFixed(2)}

Potential Savings:
  Reserved Instance (1 year): $${this.calculateReservedInstanceSavings(config).toFixed(2)}
    `;
  }
}

// Usage Example
const calculator = new EC2CostCalculator();

const config: PricingConfig = {
  instanceType: 't3.medium',
  instanceCount: 3,
  hoursPerMonth: 730,
  storageGB: 100,
  dataTransferGB: 500,
  region: 'us-east-1'
};

console.log(calculator.generateCostReport(config));

// Compare instance types
const comparison = calculator.compareInstanceTypes(
  ['t3.medium', 'm5.large', 'c5.large'],
  {
    instanceCount: 2,
    hoursPerMonth: 730,
    storageGB: 100,
    dataTransferGB: 500,
    region: 'us-east-1'
  }
);

console.log('\nInstance Type Comparison:');
comparison.forEach((cost, instanceType) => {
  console.log(`${instanceType}: $${cost.totalMonthlyCost.toFixed(2)}/month`);
});

export { EC2CostCalculator, CostBreakdown, PricingConfig };

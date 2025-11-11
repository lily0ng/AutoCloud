interface CapacityPlan {
  currentUsage: number;
  projectedGrowth: number;
  recommendedCapacity: number;
}

class CapacityPlanner {
  planCapacity(currentUsage: number, growthRate: number): CapacityPlan {
    const projectedGrowth = currentUsage * (1 + growthRate);
    const recommendedCapacity = projectedGrowth * 1.2;
    
    console.log(`📈 Capacity planning: ${currentUsage} -> ${recommendedCapacity.toFixed(0)}`);
    
    return {
      currentUsage,
      projectedGrowth,
      recommendedCapacity,
    };
  }
}

const planner = new CapacityPlanner();
const plan = planner.planCapacity(100, 0.3);
console.log(`✅ Recommended capacity: ${plan.recommendedCapacity.toFixed(0)}`);

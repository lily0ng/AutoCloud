interface CostAllocation {
  team: string;
  cost: number;
}

class CostAllocator {
  allocateCosts(totalCost: number, teams: string[]): CostAllocation[] {
    const perTeam = totalCost / teams.length;
    return teams.map(team => ({
      team,
      cost: perTeam,
    }));
  }
}

const allocator = new CostAllocator();
const allocations = allocator.allocateCosts(1000, ['team-a', 'team-b', 'team-c']);
allocations.forEach(a => console.log(`${a.team}: $${a.cost.toFixed(2)}`));

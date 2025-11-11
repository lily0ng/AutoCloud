interface VPCPeering {id: string; requester: string; accepter: string}
class PeeringManager {
  createPeering(requester: string, accepter: string): VPCPeering {
    const peering = {id: 'pcx-1', requester, accepter};
    console.log(`🔗 VPC Peering: ${requester} <-> ${accepter}`);
    return peering;
  }
}
const mgr = new PeeringManager();
mgr.createPeering('vpc-1', 'vpc-2');

type StorageTier = 'hot' | 'cool' | 'archive';
class TieringService {
  moveTo(data: string, tier: StorageTier) {
    console.log(`🔄 Moving ${data} to ${tier} tier`);
  }
}
const svc = new TieringService();
svc.moveTo('old-logs', 'archive');

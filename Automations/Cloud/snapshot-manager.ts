interface Snapshot {
  id: string;
  volumeId: string;
  createdAt: Date;
  size: number;
  description: string;
}

class SnapshotManager {
  private snapshots: Map<string, Snapshot> = new Map();
  private retentionDays: number;

  constructor(retentionDays: number = 30) {
    this.retentionDays = retentionDays;
  }

  createSnapshot(volumeId: string, description: string): Snapshot {
    const snapshot: Snapshot = {
      id: `snap-${Date.now()}`,
      volumeId,
      createdAt: new Date(),
      size: Math.floor(Math.random() * 100),
      description,
    };

    this.snapshots.set(snapshot.id, snapshot);
    console.log(`📸 Snapshot created: ${snapshot.id} for volume ${volumeId}`);

    return snapshot;
  }

  deleteSnapshot(snapshotId: string): void {
    if (this.snapshots.delete(snapshotId)) {
      console.log(`🗑️  Snapshot deleted: ${snapshotId}`);
    }
  }

  listSnapshots(volumeId?: string): Snapshot[] {
    const allSnapshots = Array.from(this.snapshots.values());

    if (volumeId) {
      return allSnapshots.filter(s => s.volumeId === volumeId);
    }

    return allSnapshots;
  }

  cleanupOldSnapshots(): void {
    console.log('🧹 Cleaning up old snapshots...');

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.retentionDays);

    let deleted = 0;

    for (const [id, snapshot] of this.snapshots) {
      if (snapshot.createdAt < cutoffDate) {
        this.deleteSnapshot(id);
        deleted++;
      }
    }

    console.log(`✅ Cleaned up ${deleted} old snapshots`);
  }

  scheduleSnapshots(volumeIds: string[], schedule: string): void {
    console.log(`⏰ Scheduling snapshots for ${volumeIds.length} volumes: ${schedule}`);

    volumeIds.forEach(volumeId => {
      this.createSnapshot(volumeId, `Scheduled snapshot - ${schedule}`);
    });
  }

  calculateStorageCost(pricePerGB: number = 0.05): number {
    const totalSize = Array.from(this.snapshots.values())
      .reduce((sum, s) => sum + s.size, 0);

    return totalSize * pricePerGB;
  }

  generateReport(): void {
    console.log('\n📊 Snapshot Report');
    console.log('==================');

    const snapshots = this.listSnapshots();
    const totalSize = snapshots.reduce((sum, s) => sum + s.size, 0);

    console.log(`Total Snapshots: ${snapshots.length}`);
    console.log(`Total Size: ${totalSize} GB`);
    console.log(`Estimated Cost: $${this.calculateStorageCost().toFixed(2)}/month`);

    console.log('\nRecent Snapshots:');
    snapshots.slice(0, 5).forEach(s => {
      console.log(`  ${s.id}: ${s.volumeId} (${s.size}GB) - ${s.createdAt.toISOString()}`);
    });
  }
}

// Example usage
const manager = new SnapshotManager(30);

manager.createSnapshot('vol-123', 'Daily backup');
manager.createSnapshot('vol-456', 'Daily backup');
manager.createSnapshot('vol-789', 'Weekly backup');

manager.scheduleSnapshots(['vol-123', 'vol-456'], 'daily at 2am');

manager.generateReport();

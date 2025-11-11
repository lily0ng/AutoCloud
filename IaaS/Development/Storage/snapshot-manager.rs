use std::collections::HashMap;
pub struct SnapshotManager {snapshots: HashMap<String, String>}
impl SnapshotManager {
    pub fn new() -> Self {SnapshotManager {snapshots: HashMap::new()}}
    pub fn create_snapshot(&mut self, volume_id: &str) -> String {
        let snap_id = format!("snap-{}", self.snapshots.len() + 1);
        self.snapshots.insert(snap_id.clone(), volume_id.to_string());
        println!("📸 Snapshot created: {}", snap_id);
        snap_id
    }
}
fn main() {
    let mut mgr = SnapshotManager::new();
    mgr.create_snapshot("vol-123");
}

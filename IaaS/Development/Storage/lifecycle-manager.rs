pub struct LifecyclePolicy {name: String, days_to_archive: u32}
impl LifecyclePolicy {
    pub fn new(name: &str, days: u32) -> Self {
        LifecyclePolicy {name: name.to_string(), days_to_archive: days}
    }
    pub fn apply(&self) {
        println!("📋 Applying lifecycle policy: {} (archive after {} days)", self.name, self.days_to_archive);
    }
}
fn main() {
    let policy = LifecyclePolicy::new("archive-old-data", 90);
    policy.apply();
}

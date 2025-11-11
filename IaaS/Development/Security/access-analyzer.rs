pub fn analyze_access(user: &str, resource: &str) -> bool {
    println!("🔍 Analyzing access: {} -> {}", user, resource);
    true
}
fn main() {
    let allowed = analyze_access("user1", "resource1");
    println!("Access allowed: {}", allowed);
}

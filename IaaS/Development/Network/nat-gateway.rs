pub struct NATGateway {pub id: String, pub subnet: String}
impl NATGateway {
    pub fn new(subnet: &str) -> Self {
        let nat = NATGateway {id: "nat-1".to_string(), subnet: subnet.to_string()};
        println!("🌐 NAT Gateway created: {} in {}", nat.id, subnet);
        nat
    }
}
fn main() {
    let nat = NATGateway::new("subnet-public");
    println!("NAT: {}", nat.id);
}

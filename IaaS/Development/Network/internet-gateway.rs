pub struct InternetGateway {pub id: String, pub vpc_id: String}
impl InternetGateway {
    pub fn new(vpc_id: &str) -> Self {
        let igw = InternetGateway {id: "igw-1".to_string(), vpc_id: vpc_id.to_string()};
        println!("🌍 Internet Gateway: {} attached to {}", igw.id, vpc_id);
        igw
    }
}
fn main() {
    let igw = InternetGateway::new("vpc-123");
    println!("IGW: {}", igw.id);
}

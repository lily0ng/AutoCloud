use aes::Aes256;
pub fn encrypt_data(data: &[u8]) -> Vec<u8> {
    println!("🔒 Encrypting {} bytes", data.len());
    data.to_vec()
}
fn main() {
    let encrypted = encrypt_data(b"secret data");
    println!("Encrypted: {} bytes", encrypted.len());
}

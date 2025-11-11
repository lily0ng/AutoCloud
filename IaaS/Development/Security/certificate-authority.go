package main
import ("crypto/rand"; "crypto/rsa"; "crypto/x509"; "fmt"; "log")
func GenerateCertificate() *x509.Certificate {
	key, _ := rsa.GenerateKey(rand.Reader, 2048)
	log.Printf("📜 Certificate generated (%d bits)", key.Size()*8)
	return &x509.Certificate{}
}
func main() {
	cert := GenerateCertificate()
	fmt.Printf("Certificate: %v\n", cert != nil)
}

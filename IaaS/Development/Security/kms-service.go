package main
import ("crypto/rand"; "fmt"; "log")
func GenerateKey() []byte {
	key := make([]byte, 32)
	rand.Read(key)
	log.Printf("🔑 Encryption key generated")
	return key
}
func main() {
	key := GenerateKey()
	fmt.Printf("Key length: %d bytes\n", len(key))
}

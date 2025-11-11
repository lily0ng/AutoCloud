package main
import ("crypto/aes"; "crypto/cipher"; "crypto/rand"; "fmt"; "io"; "log")
func Encrypt(data []byte, key []byte) ([]byte, error) {
	block, _ := aes.NewCipher(key)
	ciphertext := make([]byte, aes.BlockSize+len(data))
	iv := ciphertext[:aes.BlockSize]
	io.ReadFull(rand.Reader, iv)
	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], data)
	log.Println("🔒 Data encrypted")
	return ciphertext, nil
}
func main() {
	key := make([]byte, 32)
	rand.Read(key)
	encrypted, _ := Encrypt([]byte("secret data"), key)
	fmt.Printf("Encrypted: %d bytes\n", len(encrypted))
}

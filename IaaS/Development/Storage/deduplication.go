package main
import ("crypto/sha256"; "fmt"; "log")
type DeduplicationEngine struct {hashes map[string]bool}
func NewDedup() *DeduplicationEngine {return &DeduplicationEngine{hashes: make(map[string]bool)}}
func (d *DeduplicationEngine) IsDuplicate(data []byte) bool {
	hash := fmt.Sprintf("%x", sha256.Sum256(data))
	if d.hashes[hash] {
		log.Printf("♻️  Duplicate detected: %s", hash[:8])
		return true
	}
	d.hashes[hash] = true
	return false
}
func main() {
	dedup := NewDedup()
	data := []byte("test data")
	fmt.Printf("First: %v, Second: %v\n", dedup.IsDuplicate(data), dedup.IsDuplicate(data))
}

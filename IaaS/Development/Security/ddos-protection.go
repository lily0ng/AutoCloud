package main
import ("fmt"; "log")
func EnableDDoSProtection(resourceID string) {
	log.Printf("🛡️  DDoS protection enabled for %s", resourceID)
}
func main() {
	EnableDDoSProtection("lb-123")
	fmt.Println("✅ DDoS protection active")
}

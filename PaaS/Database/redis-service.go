package main
import ("fmt"; "log")
func CreateRedis(name string, memory int) {
	log.Printf("🔴 Redis instance created: %s (%dMB)", name, memory)
}
func main() {
	CreateRedis("cache", 512)
	fmt.Println("✅ Redis ready")
}

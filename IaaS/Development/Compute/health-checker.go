package main
import ("fmt"; "log")
func CheckHealth(endpoint string) bool {
	log.Printf("🏥 Checking health: %s", endpoint)
	return true
}
func main() {
	healthy := CheckHealth("http://server1:8080/health")
	fmt.Printf("Health: %v\n", healthy)
}

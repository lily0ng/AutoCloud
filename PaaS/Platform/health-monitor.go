package main
import ("fmt"; "log")
func MonitorHealth(app string) bool {
	log.Printf("🏥 Health check: %s", app)
	return true
}
func main() {
	healthy := MonitorHealth("my-app")
	fmt.Printf("Healthy: %v\n", healthy)
}

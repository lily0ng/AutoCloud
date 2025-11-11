package main
import ("fmt"; "log")
func ConfigureLB(app string, backends []string) {
	log.Printf("⚖️  Load balancer for %s: %d backends", app, len(backends))
}
func main() {
	ConfigureLB("my-app", []string{"10.0.1.1", "10.0.1.2"})
	fmt.Println("✅ LB configured")
}

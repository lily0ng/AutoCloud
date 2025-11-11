package main
import ("fmt"; "log")
func AddRoute(domain, app string) {
	log.Printf("🌐 Route added: %s -> %s", domain, app)
}
func main() {
	AddRoute("example.com", "my-app")
	fmt.Println("✅ Route configured")
}

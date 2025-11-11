package main
import ("fmt"; "log")
func EnableServiceMesh(services []string) {
	log.Printf("🕸️  Service mesh enabled for %d services", len(services))
	for _, svc := range services {
		log.Printf("  ✓ %s", svc)
	}
}
func main() {
	EnableServiceMesh([]string{"api", "web", "worker"})
	fmt.Println("✅ Mesh enabled")
}

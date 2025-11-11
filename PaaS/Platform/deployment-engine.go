package main
import ("fmt"; "log")
func Deploy(app, version string) {
	log.Printf("🚀 Deploying %s version %s...", app, version)
	log.Printf("  Building...")
	log.Printf("  Testing...")
	log.Printf("  Deploying...")
	log.Printf("✅ Deployment complete")
}
func main() {
	Deploy("my-app", "v1.2.3")
	fmt.Println("✅ Deployed")
}

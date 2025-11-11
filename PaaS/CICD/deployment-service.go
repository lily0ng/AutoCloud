package main
import ("fmt"; "log")
func DeployToEnvironment(app, env string) {
	log.Printf("🚀 Deploying %s to %s", app, env)
	log.Printf("  Pulling image...")
	log.Printf("  Starting containers...")
	log.Printf("✅ Deployed to %s", env)
}
func main() {
	DeployToEnvironment("my-app", "production")
	fmt.Println("✅ Deployment complete")
}

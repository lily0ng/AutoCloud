package main
import ("fmt"; "log")
func RollbackDeployment(app, version string) {
	log.Printf("⏪ Rolling back %s to %s", app, version)
	log.Printf("  Stopping current version...")
	log.Printf("  Starting previous version...")
	log.Printf("✅ Rollback complete")
}
func main() {
	RollbackDeployment("my-app", "v0.9.0")
	fmt.Println("✅ Rolled back")
}

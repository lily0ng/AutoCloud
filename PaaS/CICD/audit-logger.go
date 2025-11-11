package main
import ("fmt"; "log"; "time")
func LogDeployment(app, user, env string) {
	log.Printf("📝 Audit: %s deployed %s to %s at %s", user, app, env, time.Now().Format(time.RFC3339))
}
func main() {
	LogDeployment("my-app", "admin", "production")
	fmt.Println("✅ Audit logged")
}

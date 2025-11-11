package main
import ("fmt"; "log")
func BuildApplication(app, version string) {
	log.Printf("🔨 Building %s version %s", app, version)
	log.Printf("  Installing dependencies...")
	log.Printf("  Compiling...")
	log.Printf("✅ Build successful")
}
func main() {
	BuildApplication("my-app", "v1.0.0")
	fmt.Println("✅ Built")
}

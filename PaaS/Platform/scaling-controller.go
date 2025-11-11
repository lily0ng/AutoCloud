package main
import ("fmt"; "log")
func ScaleApp(app string, instances int) {
	log.Printf("📈 Scaling %s to %d instances", app, instances)
}
func main() {
	ScaleApp("my-app", 5)
	fmt.Println("✅ Scaled")
}

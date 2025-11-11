package main
import ("fmt"; "log")
func EmitEvent(event, data string) {
	log.Printf("📡 Event emitted: %s", event)
}
func main() {
	EmitEvent("user.created", "user-123")
	fmt.Println("✅ Event emitted")
}

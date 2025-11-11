package main
import ("fmt"; "log")
func ManageTopic(topic, action string) {
	log.Printf("📋 Topic %s: %s", action, topic)
}
func main() {
	ManageTopic("events", "create")
	fmt.Println("✅ Topic managed")
}

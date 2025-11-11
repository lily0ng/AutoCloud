package main
import ("fmt"; "log")
func Publish(channel, message string) {
	log.Printf("📢 Published to %s: %s", channel, message)
}
func main() {
	Publish("notifications", "Hello World")
	fmt.Println("✅ Message published")
}

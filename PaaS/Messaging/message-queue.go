package main
import ("fmt"; "log")
func EnqueueMessage(queue, msg string) {
	log.Printf("📥 Message enqueued to %s", queue)
}
func main() {
	EnqueueMessage("emails", "send-welcome-email")
	fmt.Println("✅ Message queued")
}

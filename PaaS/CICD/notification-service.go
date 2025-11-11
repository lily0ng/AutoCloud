package main
import ("fmt"; "log")
func SendNotification(event, message string) {
	log.Printf("📧 Notification: %s - %s", event, message)
}
func main() {
	SendNotification("deployment.success", "Deployed to production")
	fmt.Println("✅ Notification sent")
}

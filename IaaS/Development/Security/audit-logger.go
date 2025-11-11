package main
import ("fmt"; "log"; "time")
func LogAuditEvent(action, user string) {
	log.Printf("📝 Audit: %s performed %s at %s", user, action, time.Now().Format(time.RFC3339))
}
func main() {
	LogAuditEvent("CreateInstance", "admin")
	fmt.Println("✅ Audit logged")
}

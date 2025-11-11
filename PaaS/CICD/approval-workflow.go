package main
import ("fmt"; "log")
func RequestApproval(deployment string) {
	log.Printf("✋ Approval requested for: %s", deployment)
	log.Printf("  Waiting for approval...")
}
func main() {
	RequestApproval("prod-deployment")
	fmt.Println("⏳ Awaiting approval")
}

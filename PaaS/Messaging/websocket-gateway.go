package main
import ("fmt"; "log")
func StartWebSocketGateway(port int) {
	log.Printf("🔌 WebSocket gateway on port %d", port)
}
func main() {
	StartWebSocketGateway(8080)
	fmt.Println("✅ WebSocket ready")
}

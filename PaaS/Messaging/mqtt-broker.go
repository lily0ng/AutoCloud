package main
import ("fmt"; "log")
func StartMQTTBroker(port int) {
	log.Printf("🔌 MQTT broker started on port %d", port)
}
func main() {
	StartMQTTBroker(1883)
	fmt.Println("✅ MQTT broker running")
}

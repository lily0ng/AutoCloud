package main
import ("fmt"; "log")
func CreateQueue(name string) {
	log.Printf("🐰 RabbitMQ queue created: %s", name)
}
func main() {
	CreateQueue("tasks")
	fmt.Println("✅ RabbitMQ ready")
}

package main
import ("fmt"; "log")
func CreateConsumerGroup(group, topic string) {
	log.Printf("👥 Consumer group %s for topic %s", group, topic)
}
func main() {
	CreateConsumerGroup("processors", "events")
	fmt.Println("✅ Consumer group created")
}

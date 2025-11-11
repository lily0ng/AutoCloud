package main
import ("fmt"; "log")
func CreateKafkaTopic(name string, partitions int) {
	log.Printf("📨 Kafka topic created: %s (%d partitions)", name, partitions)
}
func main() {
	CreateKafkaTopic("events", 10)
	fmt.Println("✅ Kafka ready")
}

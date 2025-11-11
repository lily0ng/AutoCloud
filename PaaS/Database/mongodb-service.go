package main
import ("fmt"; "log")
func CreateMongoDB(name string, replicas int) {
	log.Printf("🍃 MongoDB cluster created: %s (%d replicas)", name, replicas)
}
func main() {
	CreateMongoDB("docs-db", 3)
	fmt.Println("✅ MongoDB ready")
}

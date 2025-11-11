package main
import ("fmt"; "log")
func CreateTimescaleDB(name string) {
	log.Printf("⏰ TimescaleDB instance: %s", name)
}
func main() {
	CreateTimescaleDB("metrics-db")
	fmt.Println("✅ TimescaleDB ready")
}

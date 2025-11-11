package main
import ("fmt"; "log")
func CreateCassandra(name string, nodes int) {
	log.Printf("💎 Cassandra cluster: %s (%d nodes)", name, nodes)
}
func main() {
	CreateCassandra("timeseries", 5)
	fmt.Println("✅ Cassandra ready")
}

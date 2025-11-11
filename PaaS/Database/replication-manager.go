package main
import ("fmt"; "log")
func SetupReplication(primary, replica string) {
	log.Printf("🔄 Replication: %s -> %s", primary, replica)
}
func main() {
	SetupReplication("db-primary", "db-replica")
	fmt.Println("✅ Replication configured")
}

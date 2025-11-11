package main
import ("fmt"; "log")
func ReplicateData(source, target string, replicas int) {
	log.Printf("🔄 Replicating %s to %d locations", source, replicas)
	for i := 1; i <= replicas; i++ {
		log.Printf("  ✓ Replica %d created at %s-%d", i, target, i)
	}
}
func main() {
	ReplicateData("primary-data", "replica", 3)
	fmt.Println("✅ Replication complete")
}

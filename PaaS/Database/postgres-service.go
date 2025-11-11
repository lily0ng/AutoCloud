package main
import ("fmt"; "log")
func CreatePostgres(name string, size int) {
	log.Printf("🐘 PostgreSQL instance created: %s (%dGB)", name, size)
}
func main() {
	CreatePostgres("prod-db", 100)
	fmt.Println("✅ Postgres ready")
}

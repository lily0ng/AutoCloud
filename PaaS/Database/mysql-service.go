package main
import ("fmt"; "log")
func CreateMySQL(name string, version string) {
	log.Printf("🐬 MySQL instance created: %s (v%s)", name, version)
}
func main() {
	CreateMySQL("app-db", "8.0")
	fmt.Println("✅ MySQL ready")
}

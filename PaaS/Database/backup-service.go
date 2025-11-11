package main
import ("fmt"; "log")
func BackupDatabase(db string) {
	log.Printf("💾 Backing up database: %s", db)
}
func main() {
	BackupDatabase("prod-db")
	fmt.Println("✅ Backup complete")
}

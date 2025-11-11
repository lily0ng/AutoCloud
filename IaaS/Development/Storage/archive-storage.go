package main
import ("fmt"; "log")
func ArchiveData(data string, tier string) string {
	archiveID := fmt.Sprintf("archive-%s", tier)
	log.Printf("🗄️  Data archived to %s tier", tier)
	return archiveID
}
func main() {
	id := ArchiveData("old-logs", "glacier")
	fmt.Printf("Archive ID: %s\n", id)
}

package main
import ("fmt"; "log"; "time")
type Backup struct {ID string; Source string; Timestamp time.Time; Size int}
func CreateBackup(source string, size int) *Backup {
	backup := &Backup{ID: fmt.Sprintf("backup-%d", time.Now().Unix()), Source: source, Timestamp: time.Now(), Size: size}
	log.Printf("💾 Backup created: %s (%dGB)", backup.ID, size)
	return backup
}
func main() {
	backup := CreateBackup("/data", 50)
	fmt.Printf("Backup: %s - %dGB\n", backup.ID, backup.Size)
}

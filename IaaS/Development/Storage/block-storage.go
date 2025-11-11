package main
import ("fmt"; "log")
type BlockVolume struct {ID string; Size int; Type string; Attached bool}
func CreateVolume(size int, volType string) *BlockVolume {
	vol := &BlockVolume{ID: fmt.Sprintf("vol-%d", size), Size: size, Type: volType, Attached: false}
	log.Printf("💾 Block volume created: %s (%dGB, %s)", vol.ID, size, volType)
	return vol
}
func main() {
	vol := CreateVolume(100, "gp3")
	fmt.Printf("Volume: %s - %dGB %s\n", vol.ID, vol.Size, vol.Type)
}

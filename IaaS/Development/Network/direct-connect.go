package main
import ("fmt"; "log")
type DirectConnect struct {ID string; Bandwidth int; Location string}
func CreateDX(bandwidth int, location string) *DirectConnect {
	dx := &DirectConnect{ID: "dx-1", Bandwidth: bandwidth, Location: location}
	log.Printf("🔌 Direct Connect: %s (%dGbps) at %s", dx.ID, bandwidth, location)
	return dx
}
func main() {
	dx := CreateDX(10, "Equinix-DC")
	fmt.Printf("DX: %s - %dGbps\n", dx.ID, dx.Bandwidth)
}

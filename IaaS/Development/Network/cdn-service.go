package main
import ("fmt"; "log")
type CDN struct {ID string; Origin string; EdgeLocations int}
func CreateCDN(origin string, edges int) *CDN {
	cdn := &CDN{ID: "cdn-1", Origin: origin, EdgeLocations: edges}
	log.Printf("🌍 CDN created: %s with origin %s (%d edges)", cdn.ID, origin, edges)
	return cdn
}
func main() {
	cdn := CreateCDN("origin.example.com", 50)
	fmt.Printf("CDN: %s - %d edge locations\n", cdn.ID, cdn.EdgeLocations)
}

package main
import ("fmt"; "log")
type LoadBalancer struct {ID string; Backends []string}
func NewLB(backends []string) *LoadBalancer {
	lb := &LoadBalancer{ID: "lb-1", Backends: backends}
	log.Printf("⚖️  Load balancer created with %d backends", len(backends))
	return lb
}
func main() {
	lb := NewLB([]string{"10.0.1.1", "10.0.1.2"})
	fmt.Printf("LB: %s\n", lb.ID)
}

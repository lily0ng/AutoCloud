package main
import ("fmt"; "log")
type Route struct {Destination string; Target string}
func AddRoute(dest, target string) *Route {
	route := &Route{Destination: dest, Target: target}
	log.Printf("🛣️  Route added: %s -> %s", dest, target)
	return route
}
func main() {
	route := AddRoute("0.0.0.0/0", "igw-123")
	fmt.Printf("Route: %s -> %s\n", route.Destination, route.Target)
}

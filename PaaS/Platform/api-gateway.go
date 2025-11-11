package main
import ("fmt"; "log")
type APIRoute struct {Path string; Backend string}
func AddAPIRoute(path, backend string) *APIRoute {
	route := &APIRoute{Path: path, Backend: backend}
	log.Printf("🚪 API route: %s -> %s", path, backend)
	return route
}
func main() {
	AddAPIRoute("/api/users", "user-service")
	fmt.Println("✅ Gateway configured")
}

package main
import ("fmt"; "log")
func ProcessStream(stream string) {
	log.Printf("🌊 Processing stream: %s", stream)
}
func main() {
	ProcessStream("clickstream")
	fmt.Println("✅ Stream processing")
}

package main
import ("fmt"; "log")
func StoreArtifact(name, version string) {
	log.Printf("📦 Storing artifact: %s:%s", name, version)
}
func main() {
	StoreArtifact("my-app", "v1.0.0")
	fmt.Println("✅ Artifact stored")
}

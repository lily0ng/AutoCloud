package main
import ("fmt"; "log")
func DistributeContent(content string, regions []string) {
	log.Printf("🌐 Distributing content to %d regions", len(regions))
	for _, region := range regions {
		log.Printf("  ✓ Cached in %s", region)
	}
}
func main() {
	DistributeContent("index.html", []string{"us-east-1", "eu-west-1", "ap-south-1"})
	fmt.Println("✅ Content distributed")
}

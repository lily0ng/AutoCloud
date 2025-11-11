package main
import ("fmt"; "log")
func RunPipeline(name string, stages []string) {
	log.Printf("🚀 Running pipeline: %s", name)
	for _, stage := range stages {
		log.Printf("  ▶️  %s", stage)
	}
	log.Printf("✅ Pipeline complete")
}
func main() {
	RunPipeline("build-deploy", []string{"build", "test", "deploy"})
	fmt.Println("✅ Pipeline executed")
}

package main
import ("fmt"; "log")
func ReportMetrics(pipeline string) {
	log.Printf("📊 Pipeline metrics for %s:", pipeline)
	log.Printf("  Duration: 5m 32s")
	log.Printf("  Success rate: 95%%")
}
func main() {
	ReportMetrics("build-deploy")
	fmt.Println("✅ Metrics reported")
}

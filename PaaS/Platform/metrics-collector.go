package main
import ("fmt"; "log")
func CollectMetrics(app string) map[string]float64 {
	metrics := map[string]float64{"cpu": 45.5, "memory": 60.2, "requests": 1250}
	log.Printf("📊 Metrics for %s: CPU %.1f%%, MEM %.1f%%", app, metrics["cpu"], metrics["memory"])
	return metrics
}
func main() {
	metrics := CollectMetrics("my-app")
	fmt.Printf("Metrics: %v\n", metrics)
}

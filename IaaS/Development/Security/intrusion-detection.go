package main
import ("fmt"; "log")
func DetectIntrusion(traffic []string) []string {
	threats := []string{}
	for _, t := range traffic {
		if len(t) > 100 {
			threats = append(threats, t)
		}
	}
	log.Printf("🚨 Detected %d potential threats", len(threats))
	return threats
}
func main() {
	threats := DetectIntrusion([]string{"normal", "suspicious_very_long_request"})
	fmt.Printf("Threats: %d\n", len(threats))
}

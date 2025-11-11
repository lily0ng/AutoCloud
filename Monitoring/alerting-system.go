package main
import ("fmt"; "log")
type Alert struct {Name string; Severity string; Condition string; Threshold float64; Actions []string}
type AlertManager struct {alerts map[string]*Alert; triggered []string}
func NewAlertManager() *AlertManager {return &AlertManager{alerts: make(map[string]*Alert), triggered: make([]string, 0)}}
func (am *AlertManager) CreateAlert(alert *Alert) {
	am.alerts[alert.Name] = alert
	log.Printf("🚨 Alert created: %s (%s)", alert.Name, alert.Severity)
}
func (am *AlertManager) CheckAlerts(metrics map[string]float64) {
	for name, alert := range am.alerts {
		if value, exists := metrics[alert.Condition]; exists && value > alert.Threshold {
			log.Printf("⚠️  Alert triggered: %s (value: %.2f, threshold: %.2f)", name, value, alert.Threshold)
			am.triggered = append(am.triggered, name)
		}
	}
}
func main() {
	manager := NewAlertManager()
	manager.CreateAlert(&Alert{Name: "HighCPU", Severity: "critical", Condition: "cpu", Threshold: 80.0, Actions: []string{"email", "slack"}})
	manager.CheckAlerts(map[string]float64{"cpu": 85.0, "memory": 60.0})
	fmt.Println("✅ Alerting system active")
}

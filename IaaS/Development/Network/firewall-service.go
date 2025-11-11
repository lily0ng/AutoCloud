package main
import ("fmt"; "log")
type FirewallRule struct {Port int; Protocol string; Action string}
func AddFirewallRule(port int, protocol, action string) *FirewallRule {
	rule := &FirewallRule{Port: port, Protocol: protocol, Action: action}
	log.Printf("🔥 Firewall rule: %s port %d -> %s", protocol, port, action)
	return rule
}
func main() {
	rule := AddFirewallRule(443, "tcp", "allow")
	fmt.Printf("Rule: %s/%d -> %s\n", rule.Protocol, rule.Port, rule.Action)
}

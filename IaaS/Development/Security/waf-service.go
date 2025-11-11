package main
import ("fmt"; "log")
type WAFRule struct {ID string; Pattern string; Action string}
func AddWAFRule(pattern, action string) *WAFRule {
	rule := &WAFRule{ID: "rule-1", Pattern: pattern, Action: action}
	log.Printf("🛡️  WAF rule added: %s -> %s", pattern, action)
	return rule
}
func main() {
	rule := AddWAFRule("SQL_INJECTION", "block")
	fmt.Printf("WAF Rule: %s\n", rule.Pattern)
}

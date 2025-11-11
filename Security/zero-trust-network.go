package main
import ("fmt"; "log")
type AccessPolicy struct {User string; Resource string; Action string; Allowed bool; Conditions map[string]string}
type ZeroTrustEngine struct {policies []AccessPolicy}
func NewZeroTrustEngine() *ZeroTrustEngine {return &ZeroTrustEngine{policies: make([]AccessPolicy, 0)}}
func (zte *ZeroTrustEngine) AddPolicy(policy AccessPolicy) {
	zte.policies = append(zte.policies, policy)
	log.Printf("🔐 Policy added: %s -> %s (%s)", policy.User, policy.Resource, policy.Action)
}
func (zte *ZeroTrustEngine) VerifyAccess(user, resource, action string) bool {
	for _, policy := range zte.policies {
		if policy.User == user && policy.Resource == resource && policy.Action == action {
			log.Printf("✅ Access granted: %s -> %s (%s)", user, resource, action)
			return policy.Allowed
		}
	}
	log.Printf("❌ Access denied: %s -> %s (%s)", user, resource, action)
	return false
}
func main() {
	zte := NewZeroTrustEngine()
	zte.AddPolicy(AccessPolicy{User: "admin", Resource: "database", Action: "read", Allowed: true})
	zte.AddPolicy(AccessPolicy{User: "user", Resource: "database", Action: "read", Allowed: false})
	zte.VerifyAccess("admin", "database", "read")
	zte.VerifyAccess("user", "database", "read")
	fmt.Println("✅ Zero Trust network active")
}

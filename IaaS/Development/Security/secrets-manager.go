package main
import ("fmt"; "log")
type Secret struct {Name string; Value string}
var secrets = make(map[string]string)
func StoreSecret(name, value string) {
	secrets[name] = value
	log.Printf("🔐 Secret stored: %s", name)
}
func GetSecret(name string) string {
	return secrets[name]
}
func main() {
	StoreSecret("db-password", "secret123")
	fmt.Printf("Secret: %s\n", GetSecret("db-password"))
}

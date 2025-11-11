package main
import ("fmt"; "log")
type User struct {ID string; Name string; Policies []string}
func CreateUser(name string, policies []string) *User {
	user := &User{ID: fmt.Sprintf("user-%s", name), Name: name, Policies: policies}
	log.Printf("👤 User created: %s with %d policies", name, len(policies))
	return user
}
func main() {
	user := CreateUser("admin", []string{"AdministratorAccess"})
	fmt.Printf("User: %s\n", user.Name)
}

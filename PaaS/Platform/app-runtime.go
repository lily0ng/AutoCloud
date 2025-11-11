package main
import ("fmt"; "log")
type Application struct {Name string; Runtime string; Instances int}
func DeployApp(name, runtime string, instances int) *Application {
	app := &Application{Name: name, Runtime: runtime, Instances: instances}
	log.Printf("🚀 App deployed: %s (%s) with %d instances", name, runtime, instances)
	return app
}
func main() {
	app := DeployApp("my-app", "nodejs18", 3)
	fmt.Printf("App: %s running on %s\n", app.Name, app.Runtime)
}

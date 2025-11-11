package main
import ("fmt"; "log")
type K8sManifest struct {Kind string; Name string; Replicas int; Image string; Port int}
func (m *K8sManifest) Generate() string {
	return fmt.Sprintf("apiVersion: apps/v1\nkind: %s\nmetadata:\n  name: %s\nspec:\n  replicas: %d\n  template:\n    spec:\n      containers:\n      - name: %s\n        image: %s\n        ports:\n        - containerPort: %d", m.Kind, m.Name, m.Replicas, m.Name, m.Image, m.Port)
}
func main() {
	manifest := &K8sManifest{Kind: "Deployment", Name: "web-app", Replicas: 3, Image: "nginx:latest", Port: 80}
	fmt.Println("📄 Kubernetes Manifest:")
	fmt.Println(manifest.Generate())
	log.Println("✅ Manifest generated")
}

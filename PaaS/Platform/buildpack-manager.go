package main
import ("fmt"; "log")
func DetectBuildpack(appType string) string {
	buildpacks := map[string]string{"nodejs": "heroku/nodejs", "python": "heroku/python", "go": "heroku/go"}
	bp := buildpacks[appType]
	log.Printf("📦 Detected buildpack: %s", bp)
	return bp
}
func main() {
	bp := DetectBuildpack("nodejs")
	fmt.Printf("Buildpack: %s\n", bp)
}

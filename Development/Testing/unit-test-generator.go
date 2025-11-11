package main
import ("fmt"; "log"; "strings")
type UnitTest struct {Name string; Function string; Input interface{}; Expected interface{}}
func GenerateTest(fn string, input, expected interface{}) string {
	testName := fmt.Sprintf("Test%s", strings.Title(fn))
	return fmt.Sprintf("func %s(t *testing.T) {\n\tgot := %s(%v)\n\tif got != %v {\n\t\tt.Errorf(\"Expected %v, got %%v\", got)\n\t}\n}", testName, fn, input, expected, expected)
}
func main() {
	test := GenerateTest("Add", "1, 2", 3)
	fmt.Println("📝 Generated Unit Test:")
	fmt.Println(test)
	log.Println("✅ Test generator ready")
}

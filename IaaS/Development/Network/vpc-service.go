package main
import ("fmt"; "log")
type VPC struct {ID string; CIDR string; Region string}
func CreateVPC(cidr, region string) *VPC {
	vpc := &VPC{ID: fmt.Sprintf("vpc-%d", 1), CIDR: cidr, Region: region}
	log.Printf("🌐 VPC created: %s (%s) in %s", vpc.ID, cidr, region)
	return vpc
}
func main() {
	vpc := CreateVPC("10.0.0.0/16", "us-east-1")
	fmt.Printf("VPC: %s - %s\n", vpc.ID, vpc.CIDR)
}

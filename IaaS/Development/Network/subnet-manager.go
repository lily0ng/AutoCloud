package main
import ("fmt"; "log")
type Subnet struct {ID string; CIDR string; AZ string}
func CreateSubnet(cidr, az string) *Subnet {
	subnet := &Subnet{ID: fmt.Sprintf("subnet-%s", az), CIDR: cidr, AZ: az}
	log.Printf("📡 Subnet created: %s (%s) in %s", subnet.ID, cidr, az)
	return subnet
}
func main() {
	subnet := CreateSubnet("10.0.1.0/24", "us-east-1a")
	fmt.Printf("Subnet: %s - %s\n", subnet.ID, subnet.CIDR)
}

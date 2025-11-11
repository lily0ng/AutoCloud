package main
import ("fmt"; "log")
type VPNGateway struct {ID string; Type string; Tunnels int}
func CreateVPN(vpnType string, tunnels int) *VPNGateway {
	vpn := &VPNGateway{ID: "vgw-1", Type: vpnType, Tunnels: tunnels}
	log.Printf("🔐 VPN gateway created: %s (%s) with %d tunnels", vpn.ID, vpnType, tunnels)
	return vpn
}
func main() {
	vpn := CreateVPN("ipsec", 2)
	fmt.Printf("VPN: %s - %d tunnels\n", vpn.ID, vpn.Tunnels)
}

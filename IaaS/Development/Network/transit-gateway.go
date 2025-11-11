package main
import ("fmt"; "log")
type TransitGateway struct {ID string; Attachments []string}
func CreateTGW(attachments []string) *TransitGateway {
	tgw := &TransitGateway{ID: "tgw-1", Attachments: attachments}
	log.Printf("🔀 Transit Gateway: %s with %d attachments", tgw.ID, len(attachments))
	return tgw
}
func main() {
	tgw := CreateTGW([]string{"vpc-1", "vpc-2", "vpn-1"})
	fmt.Printf("TGW: %s - %d attachments\n", tgw.ID, len(tgw.Attachments))
}

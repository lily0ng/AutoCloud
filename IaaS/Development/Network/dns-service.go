package main
import ("fmt"; "log")
type DNSRecord struct {Name string; Type string; Value string}
func CreateDNSRecord(name, recordType, value string) *DNSRecord {
	record := &DNSRecord{Name: name, Type: recordType, Value: value}
	log.Printf("🌐 DNS record: %s %s -> %s", name, recordType, value)
	return record
}
func main() {
	record := CreateDNSRecord("example.com", "A", "1.2.3.4")
	fmt.Printf("DNS: %s %s -> %s\n", record.Name, record.Type, record.Value)
}

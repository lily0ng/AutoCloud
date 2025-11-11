package main

import ("fmt"; "log")

type ReservedInstance struct {
	ID string; Term int; InstanceType string; Discount float64
}

func PurchaseRI(instanceType string, term int) *ReservedInstance {
	discount := 0.30
	if term == 36 { discount = 0.50 }
	ri := &ReservedInstance{
		ID: fmt.Sprintf("ri-%d", term), Term: term, InstanceType: instanceType, Discount: discount,
	}
	log.Printf("📅 Reserved instance purchased: %s for %d months (%.0f%% discount)", instanceType, term, discount*100)
	return ri
}

func main() {
	ri := PurchaseRI("t3.large", 12)
	fmt.Printf("RI: %s - %d months, %.0f%% off\n", ri.InstanceType, ri.Term, ri.Discount*100)
}

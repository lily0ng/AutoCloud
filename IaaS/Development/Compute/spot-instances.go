package main

import ("fmt"; "log")

type SpotInstance struct {
	ID string; Price float64; MaxPrice float64; Status string
}

func RequestSpotInstance(maxPrice float64) *SpotInstance {
	currentPrice := 0.05
	instance := &SpotInstance{
		ID: fmt.Sprintf("spot-%d", 1), Price: currentPrice, MaxPrice: maxPrice, Status: "running",
	}
	log.Printf("💰 Spot instance launched at $%.4f/hr (max: $%.4f)", currentPrice, maxPrice)
	return instance
}

func main() {
	spot := RequestSpotInstance(0.10)
	fmt.Printf("Spot Instance: %s - $%.4f/hr\n", spot.ID, spot.Price)
}

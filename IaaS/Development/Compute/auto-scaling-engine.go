package main

import ("fmt"; "log")

type AutoScaler struct {
	Min int; Max int; Current int; TargetCPU float64
}

func NewAutoScaler(min, max int, targetCPU float64) *AutoScaler {
	return &AutoScaler{Min: min, Max: max, Current: min, TargetCPU: targetCPU}
}

func (as *AutoScaler) Scale(currentCPU float64) {
	if currentCPU > as.TargetCPU+10 && as.Current < as.Max {
		as.Current++
		log.Printf("⬆️  Scaled up to %d instances (CPU: %.1f%%)", as.Current, currentCPU)
	} else if currentCPU < as.TargetCPU-10 && as.Current > as.Min {
		as.Current--
		log.Printf("⬇️  Scaled down to %d instances (CPU: %.1f%%)", as.Current, currentCPU)
	}
}

func main() {
	scaler := NewAutoScaler(2, 10, 70.0)
	scaler.Scale(85.0)
	fmt.Printf("Current instances: %d\n", scaler.Current)
}

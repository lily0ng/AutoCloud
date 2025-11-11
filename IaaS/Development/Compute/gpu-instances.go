package main

import ("fmt"; "log")

type GPUInstance struct {
	ID string; GPUType string; GPUCount int; Status string
}

func ProvisionGPU(gpuType string, count int) *GPUInstance {
	instance := &GPUInstance{
		ID: fmt.Sprintf("gpu-%d", count), GPUType: gpuType, GPUCount: count, Status: "running",
	}
	log.Printf("🎮 GPU instance provisioned: %s with %d x %s", instance.ID, count, gpuType)
	return instance
}

func main() {
	gpu := ProvisionGPU("NVIDIA-A100", 4)
	fmt.Printf("GPU Instance: %s - %d x %s\n", gpu.ID, gpu.GPUCount, gpu.GPUType)
}

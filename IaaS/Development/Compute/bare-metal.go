package main

import ("fmt"; "log")

type BareMetalServer struct {
	ID string; CPU int; RAM int; Disk int; Status string
}

type BareMetalProvisioner struct {
	servers map[string]*BareMetalServer
}

func NewBareMetalProvisioner() *BareMetalProvisioner {
	return &BareMetalProvisioner{servers: make(map[string]*BareMetalServer)}
}

func (bmp *BareMetalProvisioner) Provision(cpu, ram, disk int) *BareMetalServer {
	server := &BareMetalServer{
		ID: fmt.Sprintf("bm-%d", len(bmp.servers)+1), CPU: cpu, RAM: ram, Disk: disk, Status: "active",
	}
	bmp.servers[server.ID] = server
	log.Printf("🖥️  Bare metal provisioned: %s", server.ID)
	return server
}

func main() {
	provisioner := NewBareMetalProvisioner()
	server := provisioner.Provision(32, 128, 2000)
	fmt.Printf("Server: %s - %dCPU, %dGB RAM, %dGB Disk\n", server.ID, server.CPU, server.RAM, server.Disk)
}

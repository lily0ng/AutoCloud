package models

import "time"

type ClusterStatus string

const (
	ClusterCreating ClusterStatus = "creating"
	ClusterActive   ClusterStatus = "active"
	ClusterFailed   ClusterStatus = "failed"
)

type Cluster struct {
	ID        string        `json:"id"`
	Name      string        `json:"name"`
	Provider  string        `json:"provider"`
	Region    string        `json:"region"`
	Version   string        `json:"version"`
	Status    ClusterStatus `json:"status"`
	CreatedAt time.Time     `json:"created_at"`
	UpdatedAt time.Time     `json:"updated_at"`
}

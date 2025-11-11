package models

import (
	"time"
)

// DeploymentStatus represents the status of a deployment
type DeploymentStatus string

const (
	DeploymentPending    DeploymentStatus = "pending"
	DeploymentInProgress DeploymentStatus = "in_progress"
	DeploymentCompleted  DeploymentStatus = "completed"
	DeploymentFailed     DeploymentStatus = "failed"
	DeploymentRolledBack DeploymentStatus = "rolled_back"
)

// Deployment represents a cloud deployment
type Deployment struct {
	ID          string           `json:"id" bson:"_id,omitempty"`
	Name        string           `json:"name" bson:"name" validate:"required"`
	Environment string           `json:"environment" bson:"environment" validate:"required,oneof=dev staging prod"`
	Status      DeploymentStatus `json:"status" bson:"status"`
	Provider    string           `json:"provider" bson:"provider" validate:"required,oneof=aws azure gcp"`
	Region      string           `json:"region" bson:"region" validate:"required"`
	Resources   []Resource       `json:"resources" bson:"resources"`
	Config      DeploymentConfig `json:"config" bson:"config"`
	CreatedBy   string           `json:"created_by" bson:"created_by"`
	CreatedAt   time.Time        `json:"created_at" bson:"created_at"`
	UpdatedAt   time.Time        `json:"updated_at" bson:"updated_at"`
	StartedAt   *time.Time       `json:"started_at,omitempty" bson:"started_at,omitempty"`
	CompletedAt *time.Time       `json:"completed_at,omitempty" bson:"completed_at,omitempty"`
	ErrorMsg    string           `json:"error_msg,omitempty" bson:"error_msg,omitempty"`
	Metadata    map[string]interface{} `json:"metadata,omitempty" bson:"metadata,omitempty"`
}

// Resource represents a cloud resource in a deployment
type Resource struct {
	ID       string                 `json:"id" bson:"id"`
	Type     string                 `json:"type" bson:"type" validate:"required"`
	Name     string                 `json:"name" bson:"name" validate:"required"`
	Status   string                 `json:"status" bson:"status"`
	Config   map[string]interface{} `json:"config" bson:"config"`
	ARN      string                 `json:"arn,omitempty" bson:"arn,omitempty"`
	Endpoint string                 `json:"endpoint,omitempty" bson:"endpoint,omitempty"`
}

// DeploymentConfig holds deployment configuration
type DeploymentConfig struct {
	AutoScaling    bool              `json:"auto_scaling" bson:"auto_scaling"`
	MinInstances   int               `json:"min_instances" bson:"min_instances"`
	MaxInstances   int               `json:"max_instances" bson:"max_instances"`
	HealthCheck    HealthCheckConfig `json:"health_check" bson:"health_check"`
	Networking     NetworkConfig     `json:"networking" bson:"networking"`
	SecurityGroups []string          `json:"security_groups" bson:"security_groups"`
	Tags           map[string]string `json:"tags" bson:"tags"`
}

// HealthCheckConfig represents health check configuration
type HealthCheckConfig struct {
	Enabled  bool   `json:"enabled" bson:"enabled"`
	Path     string `json:"path" bson:"path"`
	Interval int    `json:"interval" bson:"interval"`
	Timeout  int    `json:"timeout" bson:"timeout"`
	Retries  int    `json:"retries" bson:"retries"`
}

// NetworkConfig represents network configuration
type NetworkConfig struct {
	VPCID           string   `json:"vpc_id" bson:"vpc_id"`
	SubnetIDs       []string `json:"subnet_ids" bson:"subnet_ids"`
	PublicAccess    bool     `json:"public_access" bson:"public_access"`
	LoadBalancerARN string   `json:"load_balancer_arn,omitempty" bson:"load_balancer_arn,omitempty"`
}

// NewDeployment creates a new deployment instance
func NewDeployment(name, environment, provider, region, createdBy string) *Deployment {
	now := time.Now()
	return &Deployment{
		Name:        name,
		Environment: environment,
		Status:      DeploymentPending,
		Provider:    provider,
		Region:      region,
		CreatedBy:   createdBy,
		CreatedAt:   now,
		UpdatedAt:   now,
		Resources:   []Resource{},
		Metadata:    make(map[string]interface{}),
	}
}

// UpdateStatus updates the deployment status
func (d *Deployment) UpdateStatus(status DeploymentStatus) {
	d.Status = status
	d.UpdatedAt = time.Now()
	
	if status == DeploymentInProgress && d.StartedAt == nil {
		now := time.Now()
		d.StartedAt = &now
	}
	
	if status == DeploymentCompleted || status == DeploymentFailed {
		now := time.Now()
		d.CompletedAt = &now
	}
}

// AddResource adds a resource to the deployment
func (d *Deployment) AddResource(resource Resource) {
	d.Resources = append(d.Resources, resource)
	d.UpdatedAt = time.Now()
}

// GetDuration returns the deployment duration
func (d *Deployment) GetDuration() time.Duration {
	if d.StartedAt == nil {
		return 0
	}
	
	endTime := time.Now()
	if d.CompletedAt != nil {
		endTime = *d.CompletedAt
	}
	
	return endTime.Sub(*d.StartedAt)
}

// IsActive checks if deployment is active
func (d *Deployment) IsActive() bool {
	return d.Status == DeploymentPending || d.Status == DeploymentInProgress
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "multicloud"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "azure_location" {
  description = "Azure region"
  type        = string
  default     = "westus2"
}

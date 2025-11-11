terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "app" {
  name        = "${var.app_name}-${var.environment}"
  description = "Application for ${var.app_name} in ${var.environment}"
}

# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "env" {
  name                = "${var.app_name}-${var.environment}"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2 v5.5.0 running Node.js 16"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = var.instance_type
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = var.min_instances
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = var.max_instances
  }
}

# RDS Database
resource "aws_db_instance" "database" {
  identifier           = "${var.app_name}-${var.environment}-db"
  allocated_storage    = 20
  engine              = "postgres"
  engine_version      = "13.7"
  instance_class      = "db.t3.micro"
  name                = var.database_name
  username            = var.database_username
  password            = var.database_password
  skip_final_snapshot = true

  tags = {
    Environment = var.environment
  }
}

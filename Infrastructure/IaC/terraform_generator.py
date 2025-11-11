"""
Terraform configuration generator
"""
import json
from typing import Dict, List


class TerraformGenerator:
    """Generate Terraform configurations dynamically"""
    
    def __init__(self, provider: str = "aws"):
        self.provider = provider
        self.resources = []
        self.variables = {}
        self.outputs = {}
    
    def add_vpc(self, name: str, cidr: str, tags: Dict = None):
        """Add VPC resource"""
        resource = {
            "resource": {
                "aws_vpc": {
                    name: {
                        "cidr_block": cidr,
                        "enable_dns_hostnames": True,
                        "enable_dns_support": True,
                        "tags": tags or {"Name": name}
                    }
                }
            }
        }
        self.resources.append(resource)
        return self
    
    def add_subnet(self, name: str, vpc_id: str, cidr: str, az: str, public: bool = False):
        """Add subnet resource"""
        resource = {
            "resource": {
                "aws_subnet": {
                    name: {
                        "vpc_id": f"${{aws_vpc.{vpc_id}.id}}",
                        "cidr_block": cidr,
                        "availability_zone": az,
                        "map_public_ip_on_launch": public,
                        "tags": {"Name": name, "Type": "Public" if public else "Private"}
                    }
                }
            }
        }
        self.resources.append(resource)
        return self
    
    def add_security_group(self, name: str, vpc_id: str, ingress: List, egress: List):
        """Add security group resource"""
        resource = {
            "resource": {
                "aws_security_group": {
                    name: {
                        "name": name,
                        "vpc_id": f"${{aws_vpc.{vpc_id}.id}}",
                        "ingress": ingress,
                        "egress": egress,
                        "tags": {"Name": name}
                    }
                }
            }
        }
        self.resources.append(resource)
        return self
    
    def add_variable(self, name: str, var_type: str, default=None, description: str = ""):
        """Add variable definition"""
        self.variables[name] = {
            "type": var_type,
            "description": description
        }
        if default is not None:
            self.variables[name]["default"] = default
        return self
    
    def add_output(self, name: str, value: str, description: str = ""):
        """Add output definition"""
        self.outputs[name] = {
            "value": value,
            "description": description
        }
        return self
    
    def generate(self) -> str:
        """Generate Terraform configuration"""
        config = {
            "terraform": {
                "required_version": ">= 1.0",
                "required_providers": {
                    self.provider: {
                        "source": f"hashicorp/{self.provider}",
                        "version": "~> 5.0"
                    }
                }
            }
        }
        
        if self.variables:
            config["variable"] = self.variables
        
        for resource in self.resources:
            config.update(resource)
        
        if self.outputs:
            config["output"] = self.outputs
        
        return json.dumps(config, indent=2)
    
    def save_to_file(self, filename: str):
        """Save configuration to file"""
        with open(filename, 'w') as f:
            f.write(self.generate())

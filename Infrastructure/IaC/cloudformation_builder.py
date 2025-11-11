"""
AWS CloudFormation template builder
"""
import yaml
from typing import Dict, List, Any


class CloudFormationBuilder:
    """Build CloudFormation templates programmatically"""
    
    def __init__(self, description: str = ""):
        self.template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": description,
            "Parameters": {},
            "Resources": {},
            "Outputs": {}
        }
    
    def add_parameter(self, name: str, param_type: str, default: Any = None, 
                     description: str = "", allowed_values: List = None):
        """Add parameter to template"""
        param = {
            "Type": param_type,
            "Description": description
        }
        if default is not None:
            param["Default"] = default
        if allowed_values:
            param["AllowedValues"] = allowed_values
        
        self.template["Parameters"][name] = param
        return self
    
    def add_vpc(self, logical_id: str, cidr: str, tags: List[Dict] = None):
        """Add VPC resource"""
        self.template["Resources"][logical_id] = {
            "Type": "AWS::EC2::VPC",
            "Properties": {
                "CidrBlock": cidr,
                "EnableDnsHostnames": True,
                "EnableDnsSupport": True,
                "Tags": tags or [{"Key": "Name", "Value": logical_id}]
            }
        }
        return self
    
    def add_subnet(self, logical_id: str, vpc_ref: str, cidr: str, az: str):
        """Add subnet resource"""
        self.template["Resources"][logical_id] = {
            "Type": "AWS::EC2::Subnet",
            "Properties": {
                "VpcId": {"Ref": vpc_ref},
                "CidrBlock": cidr,
                "AvailabilityZone": az,
                "Tags": [{"Key": "Name", "Value": logical_id}]
            }
        }
        return self
    
    def add_ec2_instance(self, logical_id: str, instance_type: str, 
                        ami_id: str, subnet_ref: str, security_groups: List):
        """Add EC2 instance resource"""
        self.template["Resources"][logical_id] = {
            "Type": "AWS::EC2::Instance",
            "Properties": {
                "InstanceType": instance_type,
                "ImageId": ami_id,
                "SubnetId": {"Ref": subnet_ref},
                "SecurityGroupIds": [{"Ref": sg} for sg in security_groups],
                "Tags": [{"Key": "Name", "Value": logical_id}]
            }
        }
        return self
    
    def add_output(self, name: str, value: Any, description: str = "", export_name: str = None):
        """Add output to template"""
        output = {
            "Value": value,
            "Description": description
        }
        if export_name:
            output["Export"] = {"Name": export_name}
        
        self.template["Outputs"][name] = output
        return self
    
    def to_yaml(self) -> str:
        """Convert template to YAML"""
        return yaml.dump(self.template, default_flow_style=False, sort_keys=False)
    
    def to_json(self) -> str:
        """Convert template to JSON"""
        import json
        return json.dumps(self.template, indent=2)
    
    def save(self, filename: str, format: str = "yaml"):
        """Save template to file"""
        with open(filename, 'w') as f:
            if format == "yaml":
                f.write(self.to_yaml())
            else:
                f.write(self.to_json())

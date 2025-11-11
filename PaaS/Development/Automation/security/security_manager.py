from cryptography.fernet import Fernet
from typing import Dict, Any
import os
import yaml
import logging
import json

class SecurityManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def generate_security_policy(self, policy_name: str) -> Dict[str, Any]:
        """Generate a basic security policy"""
        policy = {
            'name': policy_name,
            'version': '1.0',
            'rules': {
                'network': {
                    'allowed_ports': [80, 443, 22],
                    'default_action': 'deny'
                },
                'authentication': {
                    'require_mfa': True,
                    'password_policy': {
                        'min_length': 12,
                        'require_special_char': True,
                        'require_numbers': True,
                        'require_uppercase': True
                    }
                },
                'encryption': {
                    'data_at_rest': True,
                    'data_in_transit': True,
                    'key_rotation_days': 90
                },
                'compliance': {
                    'logging': {
                        'enabled': True,
                        'retention_days': 90
                    },
                    'audit': {
                        'enabled': True,
                        'interval_days': 30
                    }
                }
            }
        }
        return policy

    def encrypt_sensitive_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        try:
            return self.cipher_suite.encrypt(data.encode())
        except Exception as e:
            self.logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt_sensitive_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        try:
            return self.cipher_suite.decrypt(encrypted_data).decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {str(e)}")
            raise

    def create_security_group_rules(self, service_type: str) -> Dict[str, Any]:
        """Generate security group rules based on service type"""
        base_rules = {
            'web_app': {
                'ingress': [
                    {'port': 80, 'source': '0.0.0.0/0', 'protocol': 'tcp'},
                    {'port': 443, 'source': '0.0.0.0/0', 'protocol': 'tcp'}
                ],
                'egress': [
                    {'port': -1, 'destination': '0.0.0.0/0', 'protocol': '-1'}
                ]
            },
            'database': {
                'ingress': [
                    {'port': 5432, 'source': '10.0.0.0/8', 'protocol': 'tcp'},
                    {'port': 3306, 'source': '10.0.0.0/8', 'protocol': 'tcp'}
                ],
                'egress': [
                    {'port': -1, 'destination': '0.0.0.0/0', 'protocol': '-1'}
                ]
            }
        }
        return base_rules.get(service_type, {})

    def validate_security_config(self, config: Dict[str, Any]) -> bool:
        """Validate security configuration"""
        required_fields = ['network', 'authentication', 'encryption', 'compliance']
        try:
            return all(field in config['rules'] for field in required_fields)
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False

    def save_security_policy(self, policy: Dict[str, Any], filename: str):
        """Save security policy to file"""
        try:
            with open(filename, 'w') as f:
                yaml.dump(policy, f, default_flow_style=False)
        except Exception as e:
            self.logger.error(f"Failed to save security policy: {str(e)}")
            raise

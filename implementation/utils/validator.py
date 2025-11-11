#!/usr/bin/env python3
"""Input Validation Utilities"""

import re
from typing import Any, Dict, List

class ValidationError(Exception):
    pass

class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    @staticmethod
    def validate_port(port: int) -> bool:
        return 1 <= port <= 65535
    
    @staticmethod
    def validate_url(url: str) -> bool:
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_lower and has_digit
    
    @staticmethod
    def validate_required_fields(data: Dict, required: List[str]):
        missing = [field for field in required if field not in data]
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")
    
    @staticmethod
    def sanitize_string(s: str) -> str:
        return re.sub(r'[<>\"\'&]', '', s)

if __name__ == "__main__":
    validator = Validator()
    
    print(f"Email valid: {validator.validate_email('test@example.com')}")
    print(f"IP valid: {validator.validate_ip('192.168.1.1')}")
    print(f"Password valid: {validator.validate_password('SecurePass123')}")

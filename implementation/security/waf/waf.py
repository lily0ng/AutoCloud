#!/usr/bin/env python3
"""
Web Application Firewall (WAF) Implementation
Layer 7: Application Security
"""

import re
import logging
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WAFRule:
    def __init__(self, rule_id: str, pattern: str, action: str, description: str):
        self.rule_id = rule_id
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.action = action
        self.description = description

    def match(self, data: str) -> bool:
        return bool(self.pattern.search(data))


class WAF:
    def __init__(self):
        self.rules: List[WAFRule] = []
        self.blocked_ips: Dict[str, datetime] = {}
        self.request_counts: Dict[str, List[datetime]] = defaultdict(list)
        self.rate_limit = 100  # requests per minute
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default security rules"""
        default_rules = [
            ("SQL_INJECTION", r"(\bunion\b.*\bselect\b|\bselect\b.*\bfrom\b.*\bwhere\b)", "block", "SQL Injection Detection"),
            ("XSS", r"(<script|javascript:|onerror=|onload=)", "block", "Cross-Site Scripting Detection"),
            ("PATH_TRAVERSAL", r"(\.\./|\.\.\\)", "block", "Path Traversal Detection"),
            ("COMMAND_INJECTION", r"(;|\||&|`|\$\()", "block", "Command Injection Detection"),
            ("LDAP_INJECTION", r"(\*\)|\(\|)", "block", "LDAP Injection Detection"),
        ]

        for rule_id, pattern, action, description in default_rules:
            self.add_rule(WAFRule(rule_id, pattern, action, description))

    def add_rule(self, rule: WAFRule):
        """Add a new WAF rule"""
        self.rules.append(rule)
        logger.info(f"Added WAF rule: {rule.rule_id} - {rule.description}")

    def check_rate_limit(self, ip: str) -> bool:
        """Check if IP exceeds rate limit"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Clean old requests
        self.request_counts[ip] = [
            req_time for req_time in self.request_counts[ip]
            if req_time > minute_ago
        ]

        # Check rate limit
        if len(self.request_counts[ip]) >= self.rate_limit:
            return False

        self.request_counts[ip].append(now)
        return True

    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False

    def block_ip(self, ip: str, duration_minutes: int = 60):
        """Block an IP address"""
        block_until = datetime.now() + timedelta(minutes=duration_minutes)
        self.blocked_ips[ip] = block_until
        logger.warning(f"Blocked IP {ip} until {block_until}")

    def inspect_request(self, ip: str, method: str, path: str, 
                       headers: Dict[str, str], body: str) -> Tuple[bool, str]:
        """Inspect incoming request"""
        
        # Check if IP is blocked
        if self.is_ip_blocked(ip):
            return False, "IP_BLOCKED"

        # Check rate limit
        if not self.check_rate_limit(ip):
            self.block_ip(ip, 30)
            return False, "RATE_LIMIT_EXCEEDED"

        # Combine all request data for inspection
        request_data = f"{method} {path} {str(headers)} {body}"

        # Check against WAF rules
        for rule in self.rules:
            if rule.match(request_data):
                logger.warning(f"WAF Rule triggered: {rule.rule_id} for IP {ip}")
                if rule.action == "block":
                    self.block_ip(ip, 60)
                    return False, rule.rule_id
                elif rule.action == "log":
                    logger.info(f"Suspicious activity detected: {rule.rule_id}")

        return True, "ALLOWED"

    def get_stats(self) -> Dict:
        """Get WAF statistics"""
        return {
            "total_rules": len(self.rules),
            "blocked_ips": len(self.blocked_ips),
            "active_connections": len(self.request_counts),
        }


if __name__ == "__main__":
    waf = WAF()
    
    # Test cases
    test_requests = [
        ("192.168.1.1", "GET", "/api/users", {}, ""),
        ("192.168.1.2", "POST", "/login", {}, "username=admin' OR '1'='1"),
        ("192.168.1.3", "GET", "/search", {}, "q=<script>alert('xss')</script>"),
    ]

    for ip, method, path, headers, body in test_requests:
        allowed, reason = waf.inspect_request(ip, method, path, headers, body)
        print(f"Request from {ip}: {'ALLOWED' if allowed else 'BLOCKED'} - {reason}")

    print("\nWAF Statistics:", waf.get_stats())

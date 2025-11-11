#!/usr/bin/env python3
"""Security Compliance and Audit System"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List

class AuditLog:
    def __init__(self, log_file='audit.log'):
        self.log_file = log_file
        self.entries = []
    
    def log_event(self, user, action, resource, result, metadata=None):
        """Log an audit event"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'action': action,
            'resource': resource,
            'result': result,
            'metadata': metadata or {},
            'hash': None
        }
        
        entry['hash'] = self._calculate_hash(entry)
        self.entries.append(entry)
        self._write_to_file(entry)
        
        return entry
    
    def _calculate_hash(self, entry):
        """Calculate hash for audit entry"""
        data = json.dumps({k: v for k, v in entry.items() if k != 'hash'}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _write_to_file(self, entry):
        """Write entry to audit log file"""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def verify_integrity(self):
        """Verify audit log integrity"""
        for entry in self.entries:
            calculated_hash = self._calculate_hash(entry)
            if calculated_hash != entry['hash']:
                return False, f"Integrity check failed for entry at {entry['timestamp']}"
        return True, "All entries verified"
    
    def get_user_activity(self, user):
        """Get all activities for a specific user"""
        return [e for e in self.entries if e['user'] == user]
    
    def get_failed_actions(self):
        """Get all failed actions"""
        return [e for e in self.entries if e['result'] == 'failure']
    
    def generate_report(self):
        """Generate compliance report"""
        total = len(self.entries)
        failed = len(self.get_failed_actions())
        users = len(set(e['user'] for e in self.entries))
        
        return {
            'total_events': total,
            'failed_events': failed,
            'success_rate': ((total - failed) / total * 100) if total > 0 else 0,
            'unique_users': users,
            'report_generated': datetime.now().isoformat()
        }

if __name__ == "__main__":
    audit = AuditLog()
    
    audit.log_event('admin', 'login', '/admin', 'success')
    audit.log_event('user1', 'read', '/api/data', 'success')
    audit.log_event('user2', 'delete', '/api/resource/123', 'failure', {'reason': 'unauthorized'})
    
    print("Audit Report:", json.dumps(audit.generate_report(), indent=2))
    print("Integrity Check:", audit.verify_integrity())

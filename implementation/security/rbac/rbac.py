#!/usr/bin/env python3
"""Role-Based Access Control (RBAC) Implementation"""

from typing import Dict, List, Set
from enum import Enum

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class RBAC:
    def __init__(self):
        self.roles: Dict[str, Set[Permission]] = {}
        self.user_roles: Dict[str, Set[str]] = {}
        self._init_default_roles()
    
    def _init_default_roles(self):
        self.roles["admin"] = {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN}
        self.roles["user"] = {Permission.READ, Permission.WRITE}
        self.roles["guest"] = {Permission.READ}
    
    def assign_role(self, username: str, role: str):
        if username not in self.user_roles:
            self.user_roles[username] = set()
        self.user_roles[username].add(role)
    
    def check_permission(self, username: str, permission: Permission) -> bool:
        user_roles = self.user_roles.get(username, set())
        for role in user_roles:
            if permission in self.roles.get(role, set()):
                return True
        return False

if __name__ == "__main__":
    rbac = RBAC()
    rbac.assign_role("john", "admin")
    print(rbac.check_permission("john", Permission.DELETE))

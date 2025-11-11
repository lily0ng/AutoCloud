import os
import pwd
import grp
import crypt
import subprocess
from typing import List, Optional

class LinuxAuthManager:
    def __init__(self):
        if os.geteuid() != 0:
            raise PermissionError("Root privileges required for Linux authentication management")
            
    def create_user(self, username: str, password: str, groups: List[str] = None) -> bool:
        try:
            # Create user
            encrypted_pass = crypt.crypt(password)
            subprocess.run(['useradd', '-m', '-p', encrypted_pass, username], check=True)
            
            # Add to groups if specified
            if groups:
                for group in groups:
                    subprocess.run(['usermod', '-a', '-G', group, username], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating user: {str(e)}")
            return False
            
    def modify_user(self, username: str, new_password: Optional[str] = None, 
                   new_groups: Optional[List[str]] = None) -> bool:
        try:
            if new_password:
                encrypted_pass = crypt.crypt(new_password)
                subprocess.run(['chpasswd'], input=f"{username}:{new_password}".encode(), check=True)
                
            if new_groups:
                current_groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
                # Remove from current groups
                for group in current_groups:
                    subprocess.run(['gpasswd', '-d', username, group], check=True)
                # Add to new groups
                for group in new_groups:
                    subprocess.run(['usermod', '-a', '-G', group, username], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error modifying user: {str(e)}")
            return False
            
    def delete_user(self, username: str, remove_home: bool = False) -> bool:
        try:
            cmd = ['userdel']
            if remove_home:
                cmd.append('-r')
            cmd.append(username)
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error deleting user: {str(e)}")
            return False
            
    def verify_user(self, username: str, password: str) -> bool:
        try:
            # This is a basic check - in production, use PAM or similar
            shadow_pass = pwd.getpwnam(username).pw_passwd
            return crypt.crypt(password, shadow_pass) == shadow_pass
        except KeyError:
            return False
            
    def get_user_groups(self, username: str) -> List[str]:
        try:
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            return groups
        except KeyError:
            return []

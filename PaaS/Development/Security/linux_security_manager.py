import subprocess
import os
import logging
from typing import Dict, List, Optional
import yaml

class LinuxSecurityManager:
    def __init__(self):
        self.logger = logging.getLogger('LinuxSecurityManager')
        self.os_type = self._detect_os()

    def _detect_os(self) -> str:
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read()
                if 'ubuntu' in content.lower():
                    return 'ubuntu'
                elif 'centos' in content.lower():
                    return 'centos'
                elif 'debian' in content.lower():
                    return 'debian'
                else:
                    return 'unknown'
        except Exception:
            return 'unknown'

    def run_command(self, command: List[str]) -> tuple:
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            return stdout.decode(), stderr.decode(), process.returncode
        except Exception as e:
            self.logger.error(f"Error running command: {str(e)}")
            return "", str(e), 1

    def check_system_security(self) -> Dict:
        security_status = {
            'firewall_status': self._check_firewall(),
            'ssh_config': self._check_ssh_config(),
            'system_updates': self._check_system_updates(),
            'open_ports': self._check_open_ports(),
            'user_audit': self._audit_users()
        }
        return security_status

    def _check_firewall(self) -> Dict:
        if self.os_type == 'ubuntu' or self.os_type == 'debian':
            stdout, _, _ = self.run_command(['ufw', 'status'])
            return {'active': 'active' in stdout.lower()}
        elif self.os_type == 'centos':
            stdout, _, _ = self.run_command(['firewall-cmd', '--state'])
            return {'active': 'running' in stdout.lower()}
        return {'active': False}

    def _check_ssh_config(self) -> Dict:
        try:
            with open('/etc/ssh/sshd_config', 'r') as f:
                content = f.read()
                return {
                    'permit_root_login': 'PermitRootLogin no' in content,
                    'password_authentication': 'PasswordAuthentication no' in content,
                    'protocol_version': 'Protocol 2' in content
                }
        except Exception as e:
            self.logger.error(f"Error checking SSH config: {str(e)}")
            return {}

    def _check_system_updates(self) -> Dict:
        if self.os_type in ['ubuntu', 'debian']:
            stdout, _, _ = self.run_command(['apt', 'list', '--upgradable'])
            return {'updates_available': len(stdout.splitlines()) - 1}
        elif self.os_type == 'centos':
            stdout, _, _ = self.run_command(['yum', 'check-update', '-q'])
            return {'updates_available': len(stdout.splitlines())}
        return {'updates_available': 0}

    def _check_open_ports(self) -> List[int]:
        stdout, _, _ = self.run_command(['netstat', '-tuln'])
        ports = []
        for line in stdout.splitlines():
            if 'LISTEN' in line:
                parts = line.split()
                if ':' in parts[3]:
                    port = parts[3].split(':')[-1]
                    try:
                        ports.append(int(port))
                    except ValueError:
                        continue
        return ports

    def _audit_users(self) -> Dict:
        users = []
        try:
            with open('/etc/passwd', 'r') as f:
                for line in f:
                    if '/bin/bash' in line or '/bin/sh' in line:
                        username = line.split(':')[0]
                        users.append(username)
        except Exception as e:
            self.logger.error(f"Error auditing users: {str(e)}")
        
        return {
            'shell_users': users,
            'count': len(users)
        }

    def harden_system(self) -> bool:
        try:
            # Update system packages
            if self.os_type in ['ubuntu', 'debian']:
                self.run_command(['apt-get', 'update'])
                self.run_command(['apt-get', 'upgrade', '-y'])
            elif self.os_type == 'centos':
                self.run_command(['yum', 'update', '-y'])

            # Configure firewall
            if self.os_type in ['ubuntu', 'debian']:
                self.run_command(['ufw', 'enable'])
                self.run_command(['ufw', 'default', 'deny', 'incoming'])
                self.run_command(['ufw', 'default', 'allow', 'outgoing'])
            elif self.os_type == 'centos':
                self.run_command(['systemctl', 'start', 'firewalld'])
                self.run_command(['systemctl', 'enable', 'firewalld'])

            # Secure SSH
            ssh_config = '''
PermitRootLogin no
PasswordAuthentication no
Protocol 2
MaxAuthTries 3
PubkeyAuthentication yes
'''
            with open('/etc/ssh/sshd_config', 'a') as f:
                f.write(ssh_config)

            # Restart SSH service
            self.run_command(['systemctl', 'restart', 'sshd'])

            return True
        except Exception as e:
            self.logger.error(f"Error hardening system: {str(e)}")
            return False

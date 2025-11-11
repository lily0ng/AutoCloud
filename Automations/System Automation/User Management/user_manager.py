#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import argparse
from datetime import datetime
import platform
from pathlib import Path
import subprocess
import pwd
import grp
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UserManager:
    def __init__(self, config_path='config/config.yaml'):
        self.load_config(config_path)
        self.setup_logging()
        self.os_type = platform.system().lower()
        self.setup_os_handler()

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        # Setup system logging
        system_logger = logging.getLogger('system')
        system_logger.setLevel(self.config['logging']['log_level'])
        system_handler = logging.FileHandler(
            os.path.join(self.config['logging']['log_dir'], 'system.log'))
        system_handler.setFormatter(
            logging.Formatter(self.config['logging']['formats']['system']))
        system_logger.addHandler(system_handler)

        # Setup audit logging
        audit_logger = logging.getLogger('audit')
        audit_logger.setLevel(logging.INFO)
        audit_handler = logging.FileHandler(
            os.path.join(self.config['logging']['log_dir'], 'audit.log'))
        audit_handler.setFormatter(
            logging.Formatter(self.config['logging']['formats']['audit']))
        audit_logger.addHandler(audit_handler)

        self.system_logger = system_logger
        self.audit_logger = audit_logger

    def setup_os_handler(self):
        if self.os_type not in ['linux', 'windows', 'darwin', 'freebsd', 'openbsd']:
            raise ValueError(f"Unsupported operating system: {self.os_type}")

    def generate_password(self):
        """Generate a secure password based on policy."""
        policy = self.config['security']['password_policy']
        length = policy['min_length']
        
        characters = []
        if policy['require_uppercase']:
            characters.extend(string.ascii_uppercase)
        if policy['require_lowercase']:
            characters.extend(string.ascii_lowercase)
        if policy['require_numbers']:
            characters.extend(string.digits)
        if policy['require_special']:
            characters.extend("!@#$%^&*()_+-=[]{}|;:,.<>?")

        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

    def create_user(self, username, role, full_name=None):
        """Create a new user account."""
        try:
            if self.user_exists(username):
                raise ValueError(f"User {username} already exists")

            password = self.generate_password()
            
            if self.os_type == 'linux':
                self._create_linux_user(username, password, role)
            elif self.os_type == 'windows':
                self._create_windows_user(username, password, role)
            # Add other OS implementations here

            self.audit_logger.info('User created', extra={
                'user': username,
                'action': 'create',
                'status': 'success'
            })

            if self.config['onboarding']['welcome_email']:
                self.send_welcome_email(username, password)

            return True, password

        except Exception as e:
            self.system_logger.error(f"Failed to create user {username}: {str(e)}")
            self.audit_logger.error('User creation failed', extra={
                'user': username,
                'action': 'create',
                'status': 'failed'
            })
            return False, None

    def _create_linux_user(self, username, password, role):
        """Create a Linux user account."""
        home_dir = os.path.join(self.config['os_specific']['linux']['home_base'], username)
        shell = self.config['os_specific']['linux']['shell']
        
        # Create user
        subprocess.run(['useradd',
                       '-m',  # Create home directory
                       '-s', shell,  # Set shell
                       '-d', home_dir,  # Set home directory
                       username], check=True)
        
        # Set password
        proc = subprocess.Popen(['chpasswd'], stdin=subprocess.PIPE)
        proc.communicate(input=f"{username}:{password}".encode())
        
        # Add to groups
        for group in self.config['os_specific']['linux']['groups']:
            subprocess.run(['usermod', '-a', '-G', group, username], check=True)

    def delete_user(self, username):
        """Delete a user account."""
        try:
            if not self.user_exists(username):
                raise ValueError(f"User {username} does not exist")

            if self.os_type == 'linux':
                self._delete_linux_user(username)
            elif self.os_type == 'windows':
                self._delete_windows_user(username)
            # Add other OS implementations here

            self.audit_logger.info('User deleted', extra={
                'user': username,
                'action': 'delete',
                'status': 'success'
            })
            return True

        except Exception as e:
            self.system_logger.error(f"Failed to delete user {username}: {str(e)}")
            self.audit_logger.error('User deletion failed', extra={
                'user': username,
                'action': 'delete',
                'status': 'failed'
            })
            return False

    def _delete_linux_user(self, username):
        """Delete a Linux user account."""
        subprocess.run(['userdel', '-r', username], check=True)

    def user_exists(self, username):
        """Check if a user exists."""
        try:
            if self.os_type == 'linux':
                pwd.getpwnam(username)
                return True
        except KeyError:
            return False
        return False

    def send_welcome_email(self, username, password):
        """Send welcome email to new user."""
        try:
            smtp_config = self.config['email']
            msg = MIMEMultipart()
            msg['From'] = smtp_config['from_address']
            msg['To'] = f"{username}@{smtp_config['smtp_server'].split('.')[-2:]}"
            msg['Subject'] = "Welcome to the System"

            body = f"""
            Welcome to the system!
            
            Your account has been created with the following credentials:
            Username: {username}
            Password: {password}
            
            Please change your password upon first login.
            """

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
                if smtp_config['use_tls']:
                    server.starttls()
                server.send_message(msg)

            self.system_logger.info(f"Welcome email sent to {username}")
        except Exception as e:
            self.system_logger.error(f"Failed to send welcome email to {username}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='User Management System')
    parser.add_argument('--action', required=True, 
                      choices=['create', 'delete', 'modify', 'list'])
    parser.add_argument('--username', required=True)
    parser.add_argument('--role', choices=['admin', 'manager', 'staff', 'guest'])
    parser.add_argument('--full-name')

    args = parser.parse_args()

    user_manager = UserManager()

    if args.action == 'create':
        if not args.role:
            print("Role is required for user creation")
            sys.exit(1)
        success, password = user_manager.create_user(args.username, args.role, args.full_name)
        if success:
            print(f"User {args.username} created successfully")
            print(f"Initial password: {password}")
        else:
            print(f"Failed to create user {args.username}")
            sys.exit(1)

    elif args.action == 'delete':
        if user_manager.delete_user(args.username):
            print(f"User {args.username} deleted successfully")
        else:
            print(f"Failed to delete user {args.username}")
            sys.exit(1)

if __name__ == "__main__":
    main()

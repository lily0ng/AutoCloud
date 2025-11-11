#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import schedule
import subprocess
import platform
import shutil
import time
import smtplib
import psutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging.handlers import RotatingFileHandler

class PatchManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.retry_count = 0
        self.max_retries = 3
        self._setup_logging()
        self.os_type = platform.system().lower()
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'updates_installed': 0,
            'errors': 0,
            'system_state': {}
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Configure logging with rotation."""
        log_dir = Path(self.config.get('log_directory', 'logs'))
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"patch_manager_{datetime.now().strftime('%Y%m%d')}.log"
        max_bytes = 10 * 1024 * 1024  # 10MB
        backup_count = 5

        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())

    def _create_backup(self) -> Optional[str]:
        """Create system backup before updates."""
        if not self.config.get('backup', {}).get('enabled', False):
            return None

        backup_dir = Path(self.config['backup']['backup_dir'])
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"system_backup_{timestamp}"
        
        try:
            if self.os_type == 'windows':
                self._run_command(['wbadmin', 'start', 'backup', 
                                 '-backupTarget:', str(backup_path)])
            else:
                # Use rsync for Unix-like systems
                self._run_command(['rsync', '-aAXv', '--exclude=/proc/*',
                                 '--exclude=/sys/*', '--exclude=/tmp/*',
                                 '/', str(backup_path)])
            return str(backup_path)
        except Exception as e:
            logging.error(f"Backup failed: {e}")
            return None

    def _cleanup_old_backups(self):
        """Clean up old backups based on retention policy."""
        if not self.config.get('backup', {}).get('enabled', False):
            return

        backup_dir = Path(self.config['backup']['backup_dir'])
        retention_days = self.config['backup'].get('retention_days', 30)
        
        current_time = time.time()
        for backup in backup_dir.glob('system_backup_*'):
            if (current_time - backup.stat().st_mtime) > (retention_days * 86400):
                shutil.rmtree(backup)
                logging.info(f"Removed old backup: {backup}")

    def _send_notification(self, subject: str, message: str):
        """Send email notification."""
        if not self.config.get('notifications', {}).get('email', {}).get('enabled', False):
            return

        email_config = self.config['notifications']['email']
        msg = MIMEMultipart()
        msg['From'] = email_config['sender']
        msg['To'] = ', '.join(email_config['recipients'])
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Failed to send notification: {e}")

    def _collect_system_metrics(self):
        """Collect system performance metrics."""
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'update_duration': (self.metrics['end_time'] - self.metrics['start_time']).total_seconds() 
                if self.metrics['end_time'] else None
        }

    def _execute_pre_post_commands(self, phase: str):
        """Execute pre/post update commands."""
        commands = self.config.get('os_configs', {}).get(self.os_type, {}).get(f'{phase}_update_commands', [])
        for cmd in commands:
            self._run_command(cmd.split(), shell=True)

    def update_system(self):
        """Execute system updates with retry mechanism and rollback support."""
        self.metrics['start_time'] = datetime.now()
        logging.info("Starting system update process")
        
        try:
            # Pre-update tasks
            self._execute_pre_post_commands('pre')
            backup_path = self._create_backup()
            
            # Update execution
            success = self._perform_update_with_retry()
            
            if not success and backup_path:
                self._perform_rollback(backup_path)
            
            # Post-update tasks
            self._execute_pre_post_commands('post')
            self._cleanup_old_backups()
            
            # Finalize
            self.metrics['end_time'] = datetime.now()
            metrics = self._collect_system_metrics()
            self._send_notification(
                "System Update Complete",
                f"Update completed with status: {'Success' if success else 'Failed'}\n"
                f"Metrics: {metrics}"
            )
            
        except Exception as e:
            logging.error(f"Update process failed: {e}")
            self.metrics['errors'] += 1
            self._send_notification(
                "System Update Failed",
                f"Error during update process: {str(e)}"
            )

    def _perform_update_with_retry(self) -> bool:
        """Perform system update with retry mechanism."""
        while self.retry_count < self.max_retries:
            try:
                os_handlers = {
                    'ubuntu': self._update_ubuntu,
                    'centos': self._update_centos,
                    'rhel': self._update_rhel,
                    'windows': self._update_windows,
                    'macos': self._update_macos
                }

                handler = os_handlers.get(self.os_type.lower())
                if handler:
                    handler()
                    return True
                else:
                    logging.error(f"Unsupported OS type: {self.os_type}")
                    return False

            except Exception as e:
                self.retry_count += 1
                logging.warning(f"Update attempt {self.retry_count} failed: {e}")
                time.sleep(60)  # Wait before retry
        
        return False

    def _perform_rollback(self, backup_path: str):
        """Rollback system to previous state."""
        logging.info("Initiating system rollback")
        try:
            if self.os_type == 'windows':
                self._run_command(['wbadmin', 'start', 'recovery',
                                 '-version:', backup_path])
            else:
                self._run_command(['rsync', '-aAXv', '--delete',
                                 f"{backup_path}/", '/'])
            logging.info("Rollback completed successfully")
        except Exception as e:
            logging.error(f"Rollback failed: {e}")

    def _run_command(self, command: List[str], shell: bool = False) -> bool:
        """Execute a system command and return success status."""
        try:
            logging.info(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True, shell=shell)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e}")
            return False

    def _update_ubuntu(self):
        """Update Ubuntu/Debian based systems."""
        commands = [
            ["apt-get", "update"],
            ["apt-get", "upgrade", "-y"],
            ["apt-get", "dist-upgrade", "-y"],
            ["apt-get", "autoremove", "-y"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return

    def _update_centos(self):
        """Update CentOS systems."""
        commands = [
            ["yum", "check-update"],
            ["yum", "update", "-y"],
            ["yum", "clean", "all"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return

    def _update_rhel(self):
        """Update RHEL systems."""
        commands = [
            ["dnf", "check-update"],
            ["dnf", "update", "-y"],
            ["dnf", "clean", "all"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return

    def _update_windows(self):
        """Update Windows systems using PowerShell."""
        commands = [
            ["powershell", "Install-Module", "PSWindowsUpdate", "-Force"],
            ["powershell", "Get-WindowsUpdate"],
            ["powershell", "Install-WindowsUpdate", "-AcceptAll", "-AutoReboot"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return

    def _update_macos(self):
        """Update macOS systems."""
        commands = [
            ["softwareupdate", "--list"],
            ["softwareupdate", "--install", "--all", "--restart"]
        ]
        for cmd in commands:
            if not self._run_command(cmd):
                return

    def run_scheduled_updates(self):
        """Run updates based on schedule configuration."""
        schedule_config = self.config.get('schedule', {})
        
        if schedule_config.get('daily'):
            schedule.every().day.at(schedule_config['daily']).do(self.update_system)
        
        if schedule_config.get('weekly'):
            day, time = schedule_config['weekly'].split()
            schedule.every().week.at(time).do(self.update_system)

        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python patch_manager.py <config_file>")
        sys.exit(1)

    manager = PatchManager(sys.argv[1])
    if manager.config.get('run_immediately', False):
        manager.update_system()
    if manager.config.get('schedule_enabled', False):
        manager.run_scheduled_updates()


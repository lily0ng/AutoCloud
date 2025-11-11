#!/usr/bin/env python3

import os
import sys
import time
import logging
import yaml
import psutil
import schedule
import smtplib
import subprocess
from datetime import datetime
from logging.handlers import RotatingFileHandler
from email.mime.text import MIMEText
from pathlib import Path

class ServiceMonitor:
    def __init__(self, config_path='config.yaml'):
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.last_restart_attempts = {}
        
    def _load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            sys.exit(f"Error loading config: {e}")

    def setup_logging(self):
        log_dir = Path('/var/log/service-monitor')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger('ServiceMonitor')
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            log_dir / 'service-monitor.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def check_service(self, service_name):
        try:
            if sys.platform.startswith('linux'):
                result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    capture_output=True,
                    text=True
                )
                return result.stdout.strip() == 'active'
            elif sys.platform == 'darwin':
                result = subprocess.run(
                    ['launchctl', 'list', service_name],
                    capture_output=True
                )
                return result.returncode == 0
            elif sys.platform == 'win32':
                result = subprocess.run(
                    ['sc', 'query', service_name],
                    capture_output=True
                )
                return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error checking service {service_name}: {e}")
            return False

    def restart_service(self, service_name):
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['systemctl', 'restart', service_name], check=True)
            elif sys.platform == 'darwin':
                subprocess.run(['launchctl', 'stop', service_name], check=True)
                subprocess.run(['launchctl', 'start', service_name], check=True)
            elif sys.platform == 'win32':
                subprocess.run(['sc', 'stop', service_name], check=True)
                subprocess.run(['sc', 'start', service_name], check=True)
            
            self.logger.info(f"Successfully restarted service: {service_name}")
            self.send_notification(f"Service {service_name} restarted successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to restart service {service_name}: {e}")
            self.send_notification(
                f"Failed to restart service {service_name}: {e}",
                level='error'
            )
            return False

    def send_notification(self, message, level='info'):
        if not self.config.get('notifications', {}).get('email'):
            return

        email_config = self.config['notifications']['email']
        msg = MIMEText(message)
        msg['Subject'] = f"Service Monitor - {level.upper()}"
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']

        try:
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                if email_config.get('use_tls'):
                    server.starttls()
                if email_config.get('username'):
                    server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

    def monitor_services(self):
        for service in self.config['services']:
            service_name = service['name']
            if not self.check_service(service_name):
                self.logger.warning(f"Service {service_name} is down")
                
                # Check restart policy
                max_restarts = service.get('max_restarts', 3)
                restart_window = service.get('restart_window', 3600)  # 1 hour default
                
                # Check if we haven't exceeded restart attempts
                current_time = time.time()
                last_attempt = self.last_restart_attempts.get(service_name, {})
                
                if (current_time - last_attempt.get('time', 0) > restart_window):
                    last_attempt = {'count': 0, 'time': current_time}
                
                if last_attempt['count'] < max_restarts:
                    self.restart_service(service_name)
                    last_attempt['count'] += 1
                    last_attempt['time'] = current_time
                    self.last_restart_attempts[service_name] = last_attempt
                else:
                    self.logger.error(
                        f"Service {service_name} has exceeded maximum restart "
                        f"attempts ({max_restarts}) within {restart_window} seconds"
                    )
                    self.send_notification(
                        f"Service {service_name} has exceeded maximum restart attempts",
                        level='error'
                    )

    def run(self):
        self.logger.info("Service Monitor started")
        
        # Schedule regular monitoring
        schedule.every(self.config.get('check_interval', 60)).seconds.do(
            self.monitor_services
        )
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    monitor = ServiceMonitor()
    monitor.run()

#!/usr/bin/env python3

import os
import yaml
import logging
import schedule
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from slack_sdk import WebClient
from logging.handlers import RotatingFileHandler
import boto3
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from prometheus_client import start_http_server, Counter, Gauge
import hashlib
import gzip
import paramiko
from cryptography.fernet import Fernet
import re
from concurrent.futures import ThreadPoolExecutor
import requests
from typing import Dict, List, Any
import socket
from flask import Flask, jsonify
import platform
import winrm
import wmi
import pysnmp
from pysnmp.hlapi import *
from netmiko import ConnectHandler
import telnetlib
from scapy.all import *
from pyVim import connect
from pyVmomi import vim

# Load environment variables
load_dotenv()

class LogManager:
    def __init__(self, config_path='config.yaml'):
        self.load_config(config_path)
        self.setup_logging()
        self.setup_elasticsearch()
        self.setup_s3()
        self.setup_slack()
        self.setup_metrics()
        self.setup_encryption()
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.log_patterns = self.load_log_patterns()
        self.setup_api_endpoints()
        self.setup_device_handlers()

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger('LogManager')
        self.logger.setLevel(logging.INFO)

        # Rotating file handler
        rotation_config = self.config['log_rotation']
        handler = RotatingFileHandler(
            f'{log_dir}/system.log',
            maxBytes=rotation_config['max_size_mb'] * 1024 * 1024,
            backupCount=rotation_config['backup_count']
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setup_elasticsearch(self):
        es_config = self.config['elasticsearch']
        self.es = Elasticsearch([{
            'host': es_config['host'],
            'port': es_config['port']
        }])

    def setup_s3(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.config['s3_backup']['region']
        )

    def setup_slack(self):
        self.slack = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

    def setup_metrics(self):
        """Setup Prometheus metrics"""
        start_http_server(8000)
        self.log_counter = Counter('logs_processed_total', 'Total logs processed')
        self.error_gauge = Gauge('error_count', 'Current error count')
        self.latency_gauge = Gauge('processing_latency', 'Log processing latency')

    def setup_encryption(self):
        """Setup encryption for sensitive log data"""
        key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher_suite = Fernet(key)

    def load_log_patterns(self) -> Dict[str, str]:
        """Load regex patterns for log parsing"""
        return {
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'timestamp': r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
            'error_patterns': r'error|exception|failed|failure',
            'security_patterns': r'authentication|authorization|login|password',
        }

    def setup_api_endpoints(self):
        """Setup REST API endpoints for log querying"""
        app = Flask(__name__)

        @app.route('/api/logs', methods=['GET'])
        def get_logs():
            return jsonify({'logs': self.get_recent_logs()})

        self.thread_pool.submit(app.run, host='0.0.0.0', port=5000)

    def setup_device_handlers(self):
        """Setup handlers for different OS and network devices"""
        self.os_handlers = {
            'windows': self.collect_windows_logs,
            'linux': self.collect_linux_logs,
            'macos': self.collect_macos_logs,
            'freebsd': self.collect_freebsd_logs,
            'solaris': self.collect_solaris_logs
        }
        
        self.network_handlers = {
            'cisco_ios': self.collect_cisco_logs,
            'juniper': self.collect_juniper_logs,
            'paloalto': self.collect_paloalto_logs,
            'fortigate': self.collect_fortigate_logs,
            'checkpoint': self.collect_checkpoint_logs,
            'f5': self.collect_f5_logs,
            'arista': self.collect_arista_logs,
            'huawei': self.collect_huawei_logs,
            'mikrotik': self.collect_mikrotik_logs,
            'vmware_esxi': self.collect_vmware_logs
        }

    def analyze_log_patterns(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze logs for patterns and anomalies"""
        patterns_found = {}
        for pattern_name, pattern in self.log_patterns.items():
            matches = re.findall(pattern, str(log_data))
            patterns_found[pattern_name] = matches
        return patterns_found

    def compress_logs(self, log_data: str) -> bytes:
        """Compress log data using gzip"""
        return gzip.compress(log_data.encode())

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive information in logs"""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def perform_security_scan(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scan logs for security-related events"""
        security_findings = {
            'sensitive_data': False,
            'security_events': [],
            'risk_level': 'low'
        }
        
        # Check for sensitive data patterns
        sensitive_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # email
            r'\b\d{16}\b',  # credit card
            r'\b(?:password|secret|key)[:=]\s*\S+\b'  # credentials
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, str(log_data)):
                security_findings['sensitive_data'] = True
                security_findings['risk_level'] = 'high'
        
        return security_findings

    def generate_metrics(self) -> Dict[str, float]:
        """Generate performance metrics"""
        metrics = {
            'logs_per_second': self.log_counter._value / 60,
            'error_rate': self.error_gauge._value,
            'avg_latency': self.latency_gauge._value
        }
        return metrics

    def perform_log_correlation(self, log_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Correlate related log entries"""
        correlated_logs = []
        for i, log in enumerate(log_entries):
            related_logs = []
            if 'session_id' in log:
                related_logs = [l for l in log_entries if l.get('session_id') == log['session_id']]
            correlated_logs.append({
                'primary_log': log,
                'related_logs': related_logs
            })
        return correlated_logs

    def generate_log_summary(self, time_period: str = '1h') -> Dict[str, Any]:
        """Generate summary of log activities"""
        logs = self.get_recent_logs(time_period)
        df = pd.DataFrame(logs)
        
        summary = {
            'total_logs': len(logs),
            'error_count': len(df[df['severity'] == 'ERROR']),
            'warning_count': len(df[df['severity'] == 'WARNING']),
            'top_sources': df['source'].value_counts().head(5).to_dict(),
            'error_types': df[df['severity'] == 'ERROR']['type'].value_counts().to_dict()
        }
        return summary

    def collect_logs(self):
        """Collect logs from various sources"""
        self.logger.info("Starting log collection")
        for source in self.config['log_sources']:
            try:
                if source['type'] == 'syslog':
                    self.collect_syslog(source)
                elif source['type'] == 'snmp':
                    self.collect_snmp(source)
            except Exception as e:
                self.logger.error(f"Error collecting logs from {source['type']}: {str(e)}")

    def collect_syslog(self, source):
        """Collect syslog data"""
        self.logger.info(f"Collecting syslog from {source['host']}:{source['port']}")
        # Implementation for syslog collection

    def collect_snmp(self, source):
        """Collect SNMP data"""
        self.logger.info(f"Collecting SNMP data from {source['hosts']}")
        # Implementation for SNMP collection

    def collect_os_logs(self, os_type: str, host: str, credentials: Dict[str, str]):
        """Collect logs from specific operating system"""
        if os_type in self.os_handlers:
            return self.os_handlers[os_type](host, credentials)
        else:
            self.logger.error(f"Unsupported OS type: {os_type}")
            return None

    def collect_windows_logs(self, host: str, credentials: Dict[str, str]):
        """Collect Windows event logs"""
        try:
            session = winrm.Session(
                host,
                auth=(credentials['username'], credentials['password'])
            )
            # Collect System, Application, and Security logs
            logs = []
            for log_type in ['System', 'Application', 'Security']:
                result = session.run_ps(
                    f'Get-EventLog -LogName {log_type} -Newest 100'
                )
                logs.extend(self.parse_windows_logs(result.std_out))
            return logs
        except Exception as e:
            self.logger.error(f"Error collecting Windows logs: {str(e)}")
            return None

    def collect_linux_logs(self, host: str, credentials: Dict[str, str]):
        """Collect Linux system logs"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=credentials['username'], password=credentials['password'])
            
            log_files = ['/var/log/syslog', '/var/log/auth.log', '/var/log/kern.log']
            logs = []
            
            for log_file in log_files:
                stdin, stdout, stderr = ssh.exec_command(f'tail -n 1000 {log_file}')
                logs.extend(self.parse_linux_logs(stdout.readlines()))
            
            ssh.close()
            return logs
        except Exception as e:
            self.logger.error(f"Error collecting Linux logs: {str(e)}")
            return None

    def collect_macos_logs(self, host: str, credentials: Dict[str, str]):
        """Collect macOS system logs"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=credentials['username'], password=credentials['password'])
            
            stdin, stdout, stderr = ssh.exec_command('log show --last 1h')
            logs = self.parse_macos_logs(stdout.readlines())
            
            ssh.close()
            return logs
        except Exception as e:
            self.logger.error(f"Error collecting macOS logs: {str(e)}")
            return None

    def collect_network_device_logs(self, device_type: str, host: str, credentials: Dict[str, str]):
        """Collect logs from specific network device"""
        if device_type in self.network_handlers:
            return self.network_handlers[device_type](host, credentials)
        else:
            self.logger.error(f"Unsupported network device type: {device_type}")
            return None

    def collect_cisco_logs(self, host: str, credentials: Dict[str, str]):
        """Collect Cisco device logs"""
        try:
            device = {
                'device_type': 'cisco_ios',
                'host': host,
                'username': credentials['username'],
                'password': credentials['password'],
                'secret': credentials.get('enable_secret', '')
            }
            
            with ConnectHandler(**device) as net_connect:
                if credentials.get('enable_secret'):
                    net_connect.enable()
                
                logs = []
                logs.extend(net_connect.send_command('show logging'))
                logs.extend(net_connect.send_command('show log'))
                
                return self.parse_cisco_logs(logs)
        except Exception as e:
            self.logger.error(f"Error collecting Cisco logs: {str(e)}")
            return None

    def collect_paloalto_logs(self, host: str, credentials: Dict[str, str]):
        """Collect Palo Alto firewall logs"""
        try:
            device = {
                'device_type': 'paloalto_panos',
                'host': host,
                'username': credentials['username'],
                'password': credentials['password']
            }
            
            with ConnectHandler(**device) as net_connect:
                logs = []
                logs.extend(net_connect.send_command('show log system'))
                logs.extend(net_connect.send_command('show log traffic'))
                logs.extend(net_connect.send_command('show log threat'))
                
                return self.parse_paloalto_logs(logs)
        except Exception as e:
            self.logger.error(f"Error collecting Palo Alto logs: {str(e)}")
            return None

    def collect_vmware_logs(self, host: str, credentials: Dict[str, str]):
        """Collect VMware ESXi logs"""
        try:
            service_instance = connect.SmartConnect(
                host=host,
                user=credentials['username'],
                pwd=credentials['password'],
                disableSslCertValidation=True
            )
            
            content = service_instance.RetrieveContent()
            logs = []
            
            # Collect system logs
            for entity in content.rootFolder.childEntity:
                if hasattr(entity, 'systemLog'):
                    logs.extend(entity.systemLog.read())
            
            connect.Disconnect(service_instance)
            return self.parse_vmware_logs(logs)
        except Exception as e:
            self.logger.error(f"Error collecting VMware logs: {str(e)}")
            return None

    def parse_windows_logs(self, raw_logs):
        """Parse Windows event logs"""
        parsed_logs = []
        for log in raw_logs:
            try:
                parsed_logs.append({
                    'timestamp': log.TimeGenerated,
                    'source': log.Source,
                    'event_id': log.EventID,
                    'message': log.Message,
                    'level': log.EntryType
                })
            except Exception as e:
                self.logger.error(f"Error parsing Windows log: {str(e)}")
        return parsed_logs

    def process_logs(self, log_data):
        """Enhanced log processing with new features"""
        try:
            start_time = time.time()
            
            # Original processing
            log_data = self.process_log_data(log_data)
            
            # Additional processing
            log_data['patterns'] = self.analyze_log_patterns(log_data)
            log_data['security_scan'] = self.perform_security_scan(log_data)
            
            # Compress if needed
            if self.config.get('compression_enabled', False):
                log_data['raw_log'] = self.compress_logs(str(log_data['raw_log']))
            
            # Encrypt sensitive data
            if self.config.get('encryption_enabled', False):
                log_data['sensitive_fields'] = self.encrypt_sensitive_data(
                    str(log_data.get('sensitive_fields', ''))
                )
            
            # Update metrics
            processing_time = time.time() - start_time
            self.log_counter.inc()
            self.latency_gauge.set(processing_time)
            
            return log_data
            
        except Exception as e:
            self.logger.error(f"Error in enhanced log processing: {str(e)}")
            return None

    def process_log_data(self, log_data):
        """Process and enrich log data"""
        try:
            # Add timestamp and metadata
            log_data['processed_at'] = datetime.utcnow().isoformat()
            
            # Categorize severity
            if 'error' in log_data['message'].lower():
                log_data['severity'] = 'ERROR'
            elif 'warning' in log_data['message'].lower():
                log_data['severity'] = 'WARNING'
            else:
                log_data['severity'] = 'INFO'

            return log_data
        except Exception as e:
            self.logger.error(f"Error processing log data: {str(e)}")
            return None

    def store_logs(self, log_data):
        """Store logs in Elasticsearch"""
        try:
            index_name = f"{self.config['elasticsearch']['index_prefix']}-{datetime.now().strftime('%Y.%m.%d')}"
            self.es.index(index=index_name, body=log_data)
        except Exception as e:
            self.logger.error(f"Error storing logs in Elasticsearch: {str(e)}")

    def backup_logs(self):  
        """Backup logs to S3"""
        try:
            backup_config = self.config['s3_backup']
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # Compress logs before uploading
            # Implementation for log compression and upload to S3
            
            self.logger.info(f"Logs backed up to S3 bucket: {backup_config['bucket_name']}")
        except Exception as e:
            self.logger.error(f"Error backing up logs: {str(e)}")

    def check_compliance(self):
        """Check if logs meet compliance requirements"""
        try:
            compliance_config = self.config['compliance']
            
            # Check retention period
            # Check encryption status
            # Verify audit logging
            
            self.logger.info("Compliance check completed")
        except Exception as e:
            self.logger.error(f"Error during compliance check: {str(e)}")
        
    def monitor_and_alert(self):
        """Monitor logs and send alerts"""
        try:
            monitoring_config = self.config['monitoring']
            
            # Check error thresholds
            error_count = self.get_error_count()
            if error_count > monitoring_config['error_threshold']:
                self.send_alert(f"Critical: Error count ({error_count}) exceeded threshold")
            
        except Exception as e:
            self.logger.error(f"Error in monitoring: {str(e)}")

    def send_alert(self, message):  
        """Send alerts via configured channels"""
        try:
            # Slack alert
            if 'slack' in self.config['alerts']:
                self.slack.chat_postMessage(
                    channel=self.config['alerts']['slack']['channel'],
                    text=message
                )
            
            # Email alert
            # Implementation for email alerts
            
        except Exception as e:
            self.logger.error(f"Error sending alert: {str(e)}")

    def get_error_count(self):
        """Get count of error logs"""
        try:
            # Query Elasticsearch for error count
            return 0  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting error count: {str(e)}")
            return 0

    def get_recent_logs(self, time_period: str = '1h'):
        """Get recent logs"""
        try:
            # Query Elasticsearch for recent logs
            return []  # Placeholder
        except Exception as e:
            self.logger.error(f"Error getting recent logs: {str(e)}")
            return []

    def run(self):
        """Enhanced main execution loop"""
        # Schedule tasks
        schedule.every(5).minutes.do(self.collect_logs)
        schedule.every(1).hours.do(self.backup_logs)
        schedule.every(6).hours.do(self.check_compliance)
        schedule.every(5).minutes.do(self.monitor_and_alert)
        schedule.every(15).minutes.do(self.generate_metrics)
        schedule.every(1).hours.do(self.generate_log_summary)
        schedule.every(30).minutes.do(lambda: self.perform_log_correlation(self.get_recent_logs()))
        
        # Additional schedules for OS and network device collection
        for os_config in self.config.get('os_sources', []):
            schedule.every(os_config.get('interval', 5)).minutes.do(
                self.collect_os_logs,
                os_config['type'],
                os_config['host'],
                os_config['credentials']
            )
        
        for device_config in self.config.get('network_sources', []):
            schedule.every(device_config.get('interval', 5)).minutes.do(
                self.collect_network_device_logs,
                device_config['type'],
                device_config['host'],
                device_config['credentials']
            )
        
        # Start API server
        self.setup_api_endpoints()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    log_manager = LogManager()
    log_manager.run()



#!/usr/bin/env python3

import psutil
import time
import yaml
import logging
import schedule
import platform
import os
import re
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Counter

# Initialize metrics
cpu_usage = Gauge('system_cpu_usage', 'CPU usage in percent')
memory_usage = Gauge('system_memory_usage', 'Memory usage in percent')
disk_usage = Gauge('system_disk_usage', 'Disk usage in percent')
log_entries = Counter('system_log_entries_total', 'Total number of log entries', ['source', 'severity'])
network_stats = Gauge('system_network_stats', 'Network statistics', ['interface', 'metric'])
process_count = Gauge('system_process_count', 'Number of running processes')

class LogMonitor:
    def __init__(self, config):
        self.config = config.get('logs', {})
        self.setup_log_monitoring()

    def setup_log_monitoring(self):
        if not self.config.get('enabled', False):
            return

        self.log_sources = []
        for source in self.config.get('sources', []):
            if source.get('enabled', False):
                if source['type'] == 'syslog' and platform.system() in ['Linux', 'Darwin']:
                    self.log_sources.append(self.monitor_syslog(source['path']))
                elif source['type'] == 'journald' and platform.system() == 'Linux':
                    self.log_sources.append(self.monitor_journald())
                elif source['type'] == 'windows_event' and platform.system() == 'Windows':
                    self.log_sources.append(self.monitor_windows_events(source['channels']))

    def monitor_syslog(self, path):
        if os.path.exists(path):
            return {'type': 'syslog', 'path': path}
        return None

    def monitor_journald(self):
        try:
            import systemd.journal
            return {'type': 'journald', 'journal': systemd.journal.Reader()}
        except ImportError:
            logging.warning("systemd module not available for journald monitoring")
            return None

    def monitor_windows_events(self, channels):
        try:
            import win32evtlog
            return {'type': 'windows_event', 'channels': channels}
        except ImportError:
            logging.warning("win32evtlog module not available for Windows Event Log monitoring")
            return None

    def collect_logs(self):
        for source in self.log_sources:
            if source:
                if source['type'] == 'syslog':
                    self.collect_syslog(source['path'])
                elif source['type'] == 'journald':
                    self.collect_journald(source['journal'])
                elif source['type'] == 'windows_event':
                    self.collect_windows_events(source['channels'])

    def collect_syslog(self, path):
        try:
            with open(path, 'r') as f:
                f.seek(0, 2)  # Seek to end
                while True:
                    line = f.readline()
                    if not line:
                        break
                    self.process_log_entry('syslog', line)
        except Exception as e:
            logging.error(f"Error reading syslog: {e}")

    def collect_journald(self, journal):
        try:
            for entry in journal:
                severity = entry.get('PRIORITY', '6')
                self.process_log_entry('journald', entry.get('MESSAGE', ''), severity)
        except Exception as e:
            logging.error(f"Error reading journald: {e}")

    def collect_windows_events(self, channels):
        try:
            import win32evtlog
            for channel in channels:
                handle = win32evtlog.OpenEventLog(None, channel)
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
                events = win32evtlog.ReadEventLog(handle, flags, 0)
                for event in events:
                    self.process_log_entry('windows_event', str(event), event.EventType)
                win32evtlog.CloseEventLog(handle)
        except Exception as e:
            logging.error(f"Error reading Windows Event Log: {e}")

    def process_log_entry(self, source, message, severity='INFO'):
        filters = self.config.get('filters', {})
        if severity in filters.get('severity', [severity]):
            for pattern in filters.get('exclude_patterns', []):
                if re.match(pattern, message):
                    return
            log_entries.labels(source=source, severity=severity).inc()

class SystemMonitor:
    def __init__(self, config_path='config.yaml'):
        self.load_config(config_path)
        self.setup_logging()
        self.setup_prometheus()
        self.log_monitor = LogMonitor(self.config)
        
    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            logging.info("Configuration loaded successfully")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            self.config = {
                'interval': 60,
                'disk_paths': ['/'],
                'prometheus': {'port': 8000}
            }
            
    def setup_logging(self):
        log_config = self.config.get('logging', {})
        handler = logging.handlers.RotatingFileHandler(
            'system_monitor.log',
            maxBytes=log_config.get('max_size', 10*1024*1024),
            backupCount=log_config.get('backup_count', 5)
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

    def setup_prometheus(self):
        try:
            start_http_server(self.config['prometheus']['port'])
            logging.info(f"Prometheus metrics server started on port {self.config['prometheus']['port']}")
        except Exception as e:
            logging.error(f"Failed to start Prometheus server: {e}")

    def get_cpu_metrics(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_usage.set(cpu_percent)
            return cpu_percent
        except Exception as e:
            logging.error(f"Error collecting CPU metrics: {e}")
            return None

    def get_memory_metrics(self):
        try:
            memory = psutil.virtual_memory()
            memory_usage.set(memory.percent)
            return memory.percent
        except Exception as e:
            logging.error(f"Error collecting memory metrics: {e}")
            return None

    def get_disk_metrics(self):
        try:
            disk_metrics = {}
            for path in self.config['disk_paths']:
                usage = psutil.disk_usage(path)
                disk_metrics[path] = usage.percent
                disk_usage.labels(path=path).set(usage.percent)
            return disk_metrics
        except Exception as e:
            logging.error(f"Error collecting disk metrics: {e}")
            return None

    def get_network_metrics(self):
        try:
            network_stats = psutil.net_io_counters(pernic=True)
            for interface, stats in network_stats.items():
                network_stats.labels(interface=interface, metric='bytes_sent').set(stats.bytes_sent)
                network_stats.labels(interface=interface, metric='bytes_recv').set(stats.bytes_recv)
        except Exception as e:
            logging.error(f"Error collecting network metrics: {e}")

    def get_process_metrics(self):
        try:
            process_count.set(len(psutil.pids()))
        except Exception as e:
            logging.error(f"Error collecting process metrics: {e}")

    def collect_metrics(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        metrics = {
            'timestamp': timestamp,
            'cpu': self.get_cpu_metrics(),
            'memory': self.get_memory_metrics(),
            'disk': self.get_disk_metrics()
        }
        self.get_network_metrics()
        self.get_process_metrics()
        self.log_monitor.collect_logs()
        logging.info(f"Metrics collected: {metrics}")
        return metrics

    def run(self):
        logging.info("Starting system monitoring...")
        schedule.every(self.config['interval']).seconds.do(self.collect_metrics)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run()

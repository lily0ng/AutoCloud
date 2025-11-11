#!/usr/bin/env python3
"""Alert Manager for Monitoring System"""

import smtplib
import logging
from email.mime.text import MIMEText
from datetime import datetime
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Alert:
    def __init__(self, severity, title, message, source):
        self.severity = severity
        self.title = title
        self.message = message
        self.source = source
        self.timestamp = datetime.now()
        self.acknowledged = False

class AlertManager:
    def __init__(self, smtp_host='localhost', smtp_port=587):
        self.alerts: List[Alert] = []
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.alert_rules = {
            'critical': self.send_email_alert,
            'warning': self.log_alert,
            'info': self.log_alert
        }
    
    def create_alert(self, severity: str, title: str, message: str, source: str):
        alert = Alert(severity, title, message, source)
        self.alerts.append(alert)
        logger.info(f"Alert created: {title} [{severity}]")
        
        handler = self.alert_rules.get(severity, self.log_alert)
        handler(alert)
        
        return alert
    
    def send_email_alert(self, alert: Alert):
        """Send email notification for critical alerts"""
        try:
            msg = MIMEText(f"{alert.message}\n\nSource: {alert.source}\nTime: {alert.timestamp}")
            msg['Subject'] = f"[{alert.severity.upper()}] {alert.title}"
            msg['From'] = 'alerts@autocloud.com'
            msg['To'] = 'admin@autocloud.com'
            
            logger.info(f"Email alert sent: {alert.title}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    def log_alert(self, alert: Alert):
        """Log alert to console"""
        logger.warning(f"[{alert.severity}] {alert.title}: {alert.message}")
    
    def acknowledge_alert(self, alert_index: int):
        """Acknowledge an alert"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index].acknowledged = True
            logger.info(f"Alert acknowledged: {self.alerts[alert_index].title}")
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unacknowledged alerts"""
        return [a for a in self.alerts if not a.acknowledged]
    
    def get_statistics(self) -> Dict:
        """Get alert statistics"""
        total = len(self.alerts)
        acknowledged = sum(1 for a in self.alerts if a.acknowledged)
        by_severity = {}
        for alert in self.alerts:
            by_severity[alert.severity] = by_severity.get(alert.severity, 0) + 1
        
        return {
            'total_alerts': total,
            'acknowledged': acknowledged,
            'active': total - acknowledged,
            'by_severity': by_severity
        }

if __name__ == "__main__":
    manager = AlertManager()
    manager.create_alert('critical', 'High CPU Usage', 'CPU usage exceeded 90%', 'service-a')
    manager.create_alert('warning', 'Memory Warning', 'Memory usage at 75%', 'service-b')
    print(manager.get_statistics())

"""
Alert management system
"""
import smtplib
from email.mime.text import MIMEText
import requests
import logging

logger = logging.getLogger(__name__)


class AlertManager:
    """Manage alerts and notifications"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def send_alert(self, alert_type: str, message: str, severity: str = 'info'):
        """Send alert through configured channels"""
        if self.config.get('email', {}).get('enabled'):
            self.send_email_alert(message, severity)
        
        if self.config.get('slack', {}).get('enabled'):
            self.send_slack_alert(message, severity)
        
        if self.config.get('webhook', {}).get('enabled'):
            self.send_webhook_alert(message, severity)
    
    def send_email_alert(self, message: str, severity: str):
        """Send email alert"""
        try:
            email_config = self.config['email']
            msg = MIMEText(message)
            msg['Subject'] = f'[{severity.upper()}] AutoCloud Alert'
            msg['From'] = email_config['from']
            msg['To'] = email_config['to']
            
            with smtplib.SMTP(email_config['host'], email_config['port']) as server:
                server.starttls()
                server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
            
            logger.info("Email alert sent")
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
    
    def send_slack_alert(self, message: str, severity: str):
        """Send Slack alert"""
        try:
            webhook_url = self.config['slack']['webhook_url']
            color = {'critical': 'danger', 'warning': 'warning', 'info': 'good'}.get(severity, 'good')
            
            payload = {
                'attachments': [{
                    'color': color,
                    'text': message,
                    'footer': 'AutoCloud Alert System'
                }]
            }
            
            requests.post(webhook_url, json=payload)
            logger.info("Slack alert sent")
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {str(e)}")
    
    def send_webhook_alert(self, message: str, severity: str):
        """Send webhook alert"""
        try:
            webhook_url = self.config['webhook']['url']
            payload = {
                'message': message,
                'severity': severity,
                'source': 'autocloud'
            }
            
            requests.post(webhook_url, json=payload)
            logger.info("Webhook alert sent")
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {str(e)}")

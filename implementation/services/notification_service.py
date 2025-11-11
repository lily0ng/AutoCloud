"""
Notification service for sending alerts and messages
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Handle various notification channels"""
    
    def __init__(self, config: dict):
        self.config = config
        self.email_config = config.get('email', {})
        self.slack_config = config.get('slack', {})
        self.webhook_config = config.get('webhook', {})
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False):
        """Send email notification"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_config.get('from')
            msg['To'] = to
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(
                self.email_config.get('host'),
                self.email_config.get('port')
            ) as server:
                server.starttls()
                server.login(
                    self.email_config.get('username'),
                    self.email_config.get('password')
                )
                server.send_message(msg)
            
            logger.info(f"Email sent to {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_slack(self, channel: str, message: str, attachments: list = None):
        """Send Slack notification"""
        try:
            webhook_url = self.slack_config.get('webhook_url')
            payload = {
                'channel': channel,
                'text': message
            }
            
            if attachments:
                payload['attachments'] = attachments
            
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Slack message sent to {channel}")
            return True
        except Exception as e:
            logger.error(f"Failed to send Slack message: {str(e)}")
            return False
    
    def send_webhook(self, url: str, data: dict):
        """Send webhook notification"""
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Webhook sent to {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
            return False

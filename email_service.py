"""Email Service for sending transactional emails"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    """Handles sending of transactional emails"""
    
    def __init__(self):
        """Initialize with SMTP settings from environment"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        
    def send_reset_email(self, to_email, reset_url):
        """Send password reset email"""
        try:
            # Verify SMTP settings are configured
            if not all([self.smtp_username, self.smtp_password]):
                print("SMTP settings not configured")
                return False
                
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = 'Tilbakestill passord - Aksjeradar'
            
            # Email content
            body = f"""
            Hei!
            
            Du har bedt om å tilbakestille passordet ditt på Aksjeradar.
            
            Klikk på linken nedenfor for å lage et nytt passord:
            {reset_url}
            
            Denne linken utløper om 24 timer.
            
            Hvis du ikke ba om denne tilbakestillingen, kan du ignorere denne e-posten.
            
            Hilsen,
            Aksjeradar-teamet
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                text = msg.as_string()
                server.sendmail(self.smtp_username, to_email, text)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

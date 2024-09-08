import smtplib
from plyer import notification
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Alert:
    def __init__(self):
        pass
    
    def should_alert(self):
        pass
    
    def send_desktop_alert(self,title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon=None,  # e.g. 'path/to/icon.png'
            timeout=10,  # seconds
        )
        
    def send_alert_email(self,subject, body, to_email):
        # Configure these settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
    

while True:
    intrusion_detected = int(input())

    if intrusion_detected:
        # send_desktop_alert("Intrusion Alert", "Potential intrusion detected!")
        pass
    else:
        break

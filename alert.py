import smtplib
from plyer import notification
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import alerts_data_file
from dataFormatter import load_file,save_file
    
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
    
def send_desktop_alert(title, message):
    alerts_data = load_file(alerts_data_file)
    if alerts_data['count'] == 0:
        notification.notify(
            title=title,
            message=message,
            app_icon=None,  # e.g. 'path/to/icon.png'
            timeout=10,
        )
    elif alerts_data['count'] == 1:
        notification.notify(
            title=title,
            message=alerts_data['defaultMessage'],
            app_icon=None,
            timeout=10
        )
    else:
        return
    alerts_data['count'] = (alerts_data['count']+1)%3
    save_file(alerts_data,alerts_data_file)

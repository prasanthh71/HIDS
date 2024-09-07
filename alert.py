from plyer import notification

def send_desktop_alert(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  # e.g. 'path/to/icon.png'
        timeout=10,  # seconds
    )

while True:
    intrusion_detected = int(input())

    if intrusion_detected:
        send_desktop_alert("Intrusion Alert", "Potential intrusion detected!")
    else:
        break

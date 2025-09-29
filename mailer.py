import smtplib
from email.mime.text import MIMEText
from config import get_settings

settings = get_settings()

def send_email(to_email: str, subject: str, content: str):
    if not settings.smtp_configured:
        print("SMTP not configured.")
        return False
    try:
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = settings.email_from
        msg["To"] = to_email

        if settings.smtp_port == 465:
            with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=settings.smtp_timeout) as smtp:
                smtp.login(settings.smtp_username, settings.smtp_password)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=settings.smtp_timeout) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(settings.smtp_username, settings.smtp_password)
                smtp.send_message(msg)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

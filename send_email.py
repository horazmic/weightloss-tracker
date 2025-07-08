import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
load_dotenv()

def send_email(subject, body):
    sender_email = os.getenv("email_username")
    password = os.getenv("email_password")
    receiver_email = os.getenv("email_recipient")
    if not sender_email or not password or not receiver_email:
        raise ValueError("Email credentials are not set in the environment variables.")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as email_error:
        raise Exception(f"Failed to send email: {email_error}")
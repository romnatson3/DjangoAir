import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from django.conf import settings


def send_mail(to_email, text='', subject=''):
    msg = MIMEText(text, 'html')
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = ';'.join(to_email)
    msg['Date'] = formatdate(localtime=True)
    try:
        server_name = settings.EMAIL_SERVER_NAME
        port = settings.EMAIL_SERVER_PORT
        password = settings.EMAIL_HOST_PASSWORD
        username = settings.EMAIL_HOST_USER
        with smtplib.SMTP_SSL(server_name, port) as server:
            server.login(username, password)
            server.send_message(msg)
        logging.info(f'Send email to {to_email}')
    except Exception as e:
        logging.exception(e)

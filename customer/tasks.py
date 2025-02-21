from main.celery import app
from customer.mail import send_mail


@app.task()
def send_mail_task(email, content):
    send_mail(
        [email],
        content,
        'Airplane ticket'
    )

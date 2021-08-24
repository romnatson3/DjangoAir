from main.celery import app
from django.core.mail import EmailMessage
from django.template.loader import get_template



@app.task()
def send_mail_task(flight_data):
    template = get_template('ticket.html')
    html = template.render({'flight_data':flight_data})
    msg = EmailMessage()
    msg.subject = 'Airplane ticket'
    msg.from_email = 'info@rns.pp.ua'
    msg.to.append(flight_data['email'])
    msg.body = html
    msg.content_subtype = 'html'
    msg.send()

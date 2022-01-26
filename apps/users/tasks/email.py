from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(subject, email_to, html_alternative, text_alternative):
    msg = EmailMultiAlternatives(
        subject, text_alternative, settings.EMAIL_FROM, [email_to])
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)


@shared_task
def send_verification_email(data):
    html_template = get_template('verify/verify.html')
    text_template = get_template('alternatives/verify.txt')

    html_alternative = html_template.render(data)
    text_alternative = text_template.render(data)
    send_email('Verify your email',
               data['EMAIL'], html_alternative, text_alternative)

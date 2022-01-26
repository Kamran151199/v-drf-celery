from django.dispatch import receiver
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User
from apps.users.signals import send_verification_email
from apps.users.tasks.email import send_verification_email as send_email
from config import settings


@receiver(send_verification_email, sender=User)
def send_verification(sender, user, **kwargs):
    token = AccessToken.for_user(user)
    data = {
        'CLIENT_URL': settings.CLIENT_URL,
        'USERNAME': user.username,
        'EMAIL': user.email,
        'TOKEN': str(token),
        'ID': str(user.id)
    }
    send_email.delay(data=data)

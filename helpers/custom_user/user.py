from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings import EMAIL_VERIFICATION_REQUIRED
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    username = models.CharField(verbose_name=_('Username'), max_length=200, unique=True, )
    email = models.EmailField(verbose_name=_('Email address'), unique=True, null=False, blank=False)
    password = models.CharField(verbose_name=_('Password'), max_length=255, null=True, blank=True)
    phone_number = models.CharField(verbose_name=_('Phone number'), unique=True, null=True, blank=True, max_length=15)
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=_('Date updated'), blank=True, editable=False, auto_now=True)

    # Permission Fields
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=not EMAIL_VERIFICATION_REQUIRED)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username}({self.email})'

    def verify(self):
        self.is_verified = True
        self.save()

    class Meta:
        app_label = 'users'

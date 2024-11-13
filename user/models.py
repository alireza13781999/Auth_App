from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .validator import phone_number_validator

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_number_validator])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=15, validators=[phone_number_validator])
    code = models.CharField(max_length=6)
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)

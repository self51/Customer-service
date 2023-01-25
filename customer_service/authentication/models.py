from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_worker = models.BooleanField('worker status', default=False)
    provide_service = models.CharField(max_length=35, blank=False)

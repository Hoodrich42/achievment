from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Subscription(models.Model):
    from_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    to_user = models.ManyToManyField('auth.User', blank=True, related_name='sub')







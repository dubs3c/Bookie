""" settings models """

from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Telegram(models.Model):
    """ Telegram usernames connected to bookie users """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=50, unique=True)
    token = models.CharField(max_length=30)
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.telegram_username is None:
            self.token = get_random_string(length=5)
            self.activated = False
            return super().save(*args, **kwargs)
        else:
            return super().save(*args, **kwargs)

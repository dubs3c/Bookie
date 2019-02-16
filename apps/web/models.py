""" models """

from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Bookmarks(models.Model):
    """ Bookmarks """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

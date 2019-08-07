""" models """

import pytz

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from utils.web import is_url as check_url

class Profile(User):
    """ Extended user model """
    timezones = [(tz, tz) for tz in pytz.all_timezones]
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    timezone = models.CharField(max_length=50, default="UTC", choices=timezones)
    notifications_enabled = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """ Automatically create a profile when a user is registered """
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class Bookmarks(models.Model):
    """ Bookmarks """
    bm_id = models.CharField(max_length=7, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Make sure to generate a unique random bookmark id """
        if self.id is None:
            while True:
                random = get_random_string(7)
                if not Bookmarks.objects.filter(bm_id=random).exists():
                    self.bm_id = random
                    return super().save(*args, **kwargs)
                continue
        else:
            return super().save(*args, **kwargs)

    def is_url(self):
        """ Check the bookmark is actually a link """
        return check_url(self.link)



class ScheduledTasks(PeriodicTask):
    """ Adds additional information regarding scheduled tasks """
    periodic = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, parent_link=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

class CrontabScheduleUser(CrontabSchedule):
    """ CrontabSchedule user """
    crontab = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, parent_link=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

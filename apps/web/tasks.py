""" Celery Tasks """

from django.contrib.auth.models import User
from django.core.mail import send_mail

from apps.web.models import Bookmarks
from bookie.celery import app as celery


@celery.task(name="notify")
def notify(user_id: int):
    """ Task that notifies a user about bookmarks to read """
    user = User.objects.get(id=user_id)
    user_bookmarks = Bookmarks.objects.filter(user=user, read=False)
    send_mail(
        'Bookie - You have bookmarks to checkout!',
        f'You have {user_bookmarks.count()} unread bookmarks to read.',
        'bookie@dubell.io',
        [f'{user.email}'],
        fail_silently=False,
    )

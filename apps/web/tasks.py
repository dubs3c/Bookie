""" Celery Tasks """

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.web.models import Bookmarks
from bookie.celery import app as celery


@celery.task(bind=True, name="notify", autoretry_for=(Exception,), retry_kwargs={'max_retries': 2})
def notify(self, user_id: int):
    """ Task that notifies a user about bookmarks to read """
    try:
        user = User.objects.get(id=user_id)
        bookmarks = Bookmarks.objects.filter(user=user, read=False).order_by("?")[:5]
        msg_html = render_to_string('email/email.html', {'bookmarks': bookmarks})
        send_mail(
            'Bookie - You have bookmarks to checkout!',
            "message",
            'bookie@dubell.io',
            [f'{user.email}'],
            fail_silently=False,
            html_message=msg_html
        )
    except Exception as exc:
        raise self.retry(exc=exc)

""" Celery Tasks """

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.web.models import Bookmarks, ActivationTokens, ScheduledTasks
from bookie.celery import app as celery


@celery.task(
    bind=True,
    name="notify",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 2},
)
def notify(self, user_id: int):
    """ Task that notifies a user about bookmarks to read """
    try:
        user = User.objects.get(id=user_id)
        task = ScheduledTasks.objects.filter(user=user)
        if task:
            if not task[0].enabled:
                return
        bookmarks = Bookmarks.objects.filter(user=user, read=False).order_by("?")[:5]
        if bookmarks:
            msg_html = render_to_string("email/email.html", {"bookmarks": bookmarks})
            send_mail(
                "Bookie - You have bookmarks to checkout!",
                "message",
                "bookie@dubell.io",
                [f"{user.email}"],
                fail_silently=False,
                html_message=msg_html,
            )
    except Exception as exc:
        raise self.retry(exc=exc)


@celery.task(
    bind=True,
    name="activation_code",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 2},
)
def send_activation_code(self, user_id: int):
    """ Task that sends an activation code to the users email """
    try:
        token = ActivationTokens.objects.get(user__id=user_id)
        msg_html = render_to_string(
            "registration/activation.html", {"code": token.code}
        )
        send_mail(
            "Bookie - Please activate your account",
            "message",
            "bookie@dubell.io",
            [f"{token.user.email}"],
            fail_silently=False,
            html_message=msg_html,
        )
    except Exception as exc:
        raise self.retry(exc=exc)

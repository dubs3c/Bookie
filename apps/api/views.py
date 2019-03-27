""" APIs """

from datetime import timedelta
import logging
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from apps.settings.models import Telegram
from apps.web.models import Bookmarks
from utils.web import is_url, parse_article
from utils.telegram import send_message


LOGGER = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
def telegram_api(request):
    """ Add bookmarks via telegram """

    if request.method == "POST":
        data = json.loads(request.body.decode())
        LOGGER.debug(data)

        try:
            telegram_username = data["message"]["from"]["username"]
            content = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
        except KeyError as error:
            LOGGER.error(error)
            return HttpResponse(status=400)

        if content.startswith("/register"):
            cmd = content.split(" ")

            if len(cmd) == 1:
                send_message(chat_id, "You forgot to enter your code...")
                return HttpResponse(status=200)

            token = cmd[1]

            token_exists = get_object_or_404(Telegram, token=token, activated=False)

            if token_exists.created < (token_exists.created + timedelta(minutes=3)):
                token_exists.activated = True
                token_exists.save()
                result, msg = send_message(chat_id, "Success, your telegram account is now linked to Bookie!")
                if not result:
                    LOGGER.error(f"Could not send message to telegram user, status code: {msg}")
                LOGGER.info(f"User \"{token_exists.user.username}\" activated telegram integration")
                return HttpResponse(status=201)
            else:
                token_exists.token = get_random_string(length=5)
                token_exists.save()
                result, msg = send_message(chat_id, "Your token has expired, a new one has been generted.")
                if not result:
                    LOGGER.error(f"Could send message to telegram user, status code: {msg}")
                LOGGER.info(f"User \"{token_exists.user.username}\" failed telegram integration, \
                            token expired")
                return HttpResponse(status=200)

        telegram = get_object_or_404(Telegram, telegram_username=telegram_username)

        if is_url(content):
            parsed_html = parse_article(content)
            Bookmarks.objects.create(user=telegram.user, link=content, 
                                     description=parsed_html["description"],
                                     title=parsed_html["title"],
                                     image=parsed_html["image"])
        else:
            Bookmarks.objects.create(user=telegram.user, link=content)

        return HttpResponse(status="201")

    if request.method == "GET":
        return HttpResponse("yer a wizard, harry", content_type="text/plain")

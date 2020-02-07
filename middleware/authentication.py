""" Custom authentication middleware """

from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse

def is_authenticated(get_response):
    """ Check if user is authenticated """
    whitelist = ["/login/", "/logout/", "/register/", "/api/", "/activate/"]

    def middleware(request):

        if not request.user.is_authenticated and True not in [x in request.path for x in whitelist]:
            return redirect(reverse("login"))

        response = get_response(request)

        return response
    return middleware

"""bookie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from apps.web.views import index, user_login, user_logout, register


urlpatterns = [
    path('', index, name="index"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('register/', register, name="register"),
    path("api/", include('apps.api.urls')),
    path('dashboard/', include('apps.web.urls')),
    path('settings/', include('apps.settings.urls')),
    path('admin/', admin.site.urls),
]

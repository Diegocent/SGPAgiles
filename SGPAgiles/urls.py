from django.urls import path
from django.contrib import admin

from login.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login),
]

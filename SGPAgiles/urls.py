from django.urls import path, include
from django.contrib import admin

from login.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login),
    path('accounts/', include('allauth.urls')),

]

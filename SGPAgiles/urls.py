from django.urls import path, include
from django.contrib import admin

import proyecto
from login.views import login
from .views import Home
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login),
    path('', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('proyecto/', include('proyecto.urls')),
    path('config/', include('Usuario.urls')),
    path('', Home.as_view(), name="home"),
]

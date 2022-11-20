from django.urls import path, include
from django.contrib import admin

import proyecto
from login.views import login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name="home"),
    path('accounts/', include('allauth.urls')),
    path('proyecto/', include('proyecto.urls')),
    path('config/', include('Usuario.urls')),
    path('notificaciones/', include('notificaciones.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

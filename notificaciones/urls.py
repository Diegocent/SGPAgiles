from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificacionesPageView.as_view(), name='ver_notificaciones'),
]

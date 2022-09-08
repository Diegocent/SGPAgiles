from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.CrearProyectoView.as_view(), name='crear'),
]
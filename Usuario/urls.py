from django.urls import path
from . import views

urlpatterns = [
    path('crear_permiso', views.CrearPermisoView.as_view(), name='crear'),
    path('crear_roles', views.CrearRolSistemaView.as_view(), name='crear_rol'),
    path('asignar_rol', views.AsignarRolSistemaView.as_view(), name='asignar_rol'),
]
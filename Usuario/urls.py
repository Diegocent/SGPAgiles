from django.urls import path
from . import views

urlpatterns = [
    path('', views.VerConfigView.as_view(), name='ver_config'),
    path('crear_permiso/', views.CrearPermisoView.as_view(), name='crear'),
    path('crear_roles/', views.CrearRolSistemaView.as_view(), name='crear_rol'),
    path('asignar_rol/', views.AsignarRolSistemaView.as_view(), name='asignar_rol'),
    path('ver_roles/', views.VerRolesSistemaView.as_view(), name='ver_roles_sistema'),
    path('ver_permisos/', views.VerPermisosView.as_view(), name='ver_permisos'),
    path('usuarios_con_roles/', views.VerUsuariosConRolesView.as_view(), name='usuarios_con_roles'),
]
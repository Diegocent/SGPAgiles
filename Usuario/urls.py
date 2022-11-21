from django.urls import path
from . import views

urlpatterns = [
    path('', views.VerConfigView.as_view(), name='ver_config'),
    path('permisos/crear', views.CrearPermisoView.as_view(), name='crear_permiso'),
    path('roles/crear', views.CrearRolSistemaView.as_view(), name='crear_rol_sistema'),
    path('roles/asignar', views.AsignarRolSistemaView.as_view(), name='asignar_rol_sistema'),
    path('roles/', views.VerRolesSistemaView.as_view(), name='ver_roles_sistema'),
    path('permisos/', views.VerPermisosView.as_view(), name='ver_permisos'),
    path('usuarios_con_roles/', views.VerUsuariosConRolesView.as_view(), name='usuarios_con_roles'),
    path('roles/<int:id_rol>/editar/', views.EditarRolSistemaView.as_view(), name='editar_rol_sistema'),
]
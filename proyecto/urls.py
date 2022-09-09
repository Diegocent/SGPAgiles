from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.CrearProyectoView.as_view(), name='crear'),
    path('', views.VerProyectosView.as_view(), name='ver_proyectos'),
    path('<int:id_proyecto>/', views.VerProyectoView.as_view(), name='detalle_proyecto'),
    path('<int:id_proyecto>/crear_equipo', views.CrearEquipoView.as_view(), name='crear_equipo'),
    path('<int:id_proyecto>/iniciar_proyecto', views.IniciarProyectoView.as_view(), name='iniciar_proyecto'),
    path('<int:id_proyecto>/crear_rol_proyecto', views.CrearRolProyectoView.as_view(), name='crear_rol_proyecto'),
    path('<int:id_proyecto>/ver_roles', views.VerRolesProyectoView.as_view(), name='ver_roles'),

]
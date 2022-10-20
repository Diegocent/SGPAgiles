from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.CrearProyectoView.as_view(), name='crear'),
    path('', views.VerProyectosView.as_view(), name='ver_proyectos'),
    path('<int:id_proyecto>/', views.VerProyectoView.as_view(), name='detalle_proyecto'),
    path('<int:id_proyecto>/crear_equipo/', views.CrearEquipoView.as_view(), name='crear_equipo'),
    path('<int:id_proyecto>/iniciar_proyecto/', views.IniciarProyectoView.as_view(), name='iniciar_proyecto'),
    path('<int:id_proyecto>/crear_rol_proyecto/', views.CrearRolProyectoView.as_view(), name='crear_rol_proyecto'),
    path('<int:id_proyecto>/ver_roles/', views.VerRolesProyectoView.as_view(), name='ver_roles'),
    path('<int:id_proyecto>/backlog/tipoUS/', views.VerTiposdeUSView.as_view(), name='tiposUS'),
    path('<int:id_proyecto>/backlog/tipoUS/crear/', views.CrearTiposUSView.as_view(), name='crear_tipoUS'),
    path('<int:id_proyecto>/backlog/tipoUS/<int:id_tipous>/', views.DetalleTiposUSView.as_view(), name='detalle_tipoUS'),
    path('<int:id_proyecto>/backlog/tipoUS/<int:id_tipous>/crear_estadoUS/', views.CrearEstadosUSView.as_view(), name='crear_estadoUS'),
    path('<int:id_proyecto>/backlog/US/crear_US/', views.CrearUSView.as_view(), name='crear_US'),
    path('<int:id_proyecto>/backlog/US/', views.VerUSView.as_view(), name='ver_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/', views.ActualizarUSView.as_view(), name='editar_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/borrar/', views.BorrarUSView.as_view(), name='borrar_US'),
    path('<int:id_proyecto>/equipo/<int:id_equipo>/', views.DetalleEquipoView.as_view(), name='ver_equipo'),
    path('<int:id_proyecto>/equipo/<int:id_equipo>/editar/', views.ActualizarEquipoView.as_view(), name='editar_equipo'),
    path('<int:id_proyecto>/sprint/crear/', views.CrearSprint.as_view(), name='crear_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/', views.DetalleSprintView.as_view(), name='ver_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/asignar_miembros/', views.AsignarMiembroASprint.as_view(), name='asignar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/editar_miembro/<int:id_miembrosprint>',
         views.ActualizarMiembrosSprintView.as_view(), name='asignar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/eliminar_miembro/<int:id_miembrosprint>',
         views.BorrarMiembrosSprintView.as_view(), name='eliminar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/asignar_us/', views.AsignarUSASprint.as_view(), name='asignar_us_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/eliminar_us/<int:id_us>/', views.BorrarUSASprint.as_view(), name='eliminar_us_sprint'),
    path('<int:id_proyecto>/backlog/', views.verProductBacklog.as_view(), name='ver_product_backlog'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('crear', views.CrearProyectoView.as_view(), name='crear'),
    path('', views.VerProyectosView.as_view(), name='ver_proyectos'),
    path('<int:id_proyecto>/', views.VerProyectoView.as_view(), name='detalle_proyecto'),
    path('<int:id_proyecto>/backlog/importar/', views.ImportarMainPageView.as_view(), name='importar'),
    path('<int:id_proyecto>/backlog/importar/<int:id_proyecto_a_importar>/roles', views.ImportarRolesDeOtroProyectoView.as_view(), name='importar_roles'),
    path('<int:id_proyecto>/backlog/importar/<int:id_proyecto_a_importar>/tipos', views.ImportarTiposUSDeOtroProyectoView.as_view(), name='importar_tipos'),
    path('<int:id_proyecto>/equipo/crear/', views.CrearEquipoView.as_view(), name='crear_equipo'),
    path('<int:id_proyecto>/iniciar/', views.IniciarProyectoView.as_view(), name='iniciar_proyecto'),
    path('<int:id_proyecto>/roles/crear/', views.CrearRolProyectoView.as_view(), name='crear_rol_proyecto'),
    path('<int:id_proyecto>/roles/', views.VerRolesProyectoView.as_view(), name='ver_roles'),
    path('<int:id_proyecto>/roles/<int:id_rol>/', views.VerRolesProyectoView.as_view(), name='detalle_roles'), #TODO cambiar vista.
    path('<int:id_proyecto>/roles/<int:id_rol>/editar/', views.ActualizarRolProyecto.as_view(), name='editar_roles'),
    path('<int:id_proyecto>/backlog/tipoUS/', views.VerTiposdeUSView.as_view(), name='tiposUS'),
    path('<int:id_proyecto>/backlog/tipoUS/crear/', views.CrearTiposUSView.as_view(), name='crear_tipoUS'),
    path('<int:id_proyecto>/backlog/tipoUS/<int:id_tipous>/', views.DetalleTiposUSView.as_view(), name='detalle_tipoUS'),
    path('<int:id_proyecto>/backlog/tipoUS/<int:id_tipous>/crear_estadoUS/', views.CrearEstadosUSView.as_view(), name='crear_estadoUS'),
    path('<int:id_proyecto>/backlog/US/crear/', views.CrearUSView.as_view(), name='crear_US'),
    path('<int:id_proyecto>/backlog/US/', views.VerUSView.as_view(), name='ver_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/', views.DetalleUSView.as_view(), name='detalle_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/editar/', views.ActualizarUSView.as_view(), name='editar_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/borrar/', views.BorrarUSView.as_view(), name='borrar_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/cargar_trabajo/', views.AgregarTrabajoAUserStory.as_view(),
         name='cargar_trabajo_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/solicitar_aprobacion/', views.SolicitarAprobacionDeUS.as_view(),
         name='solicitar_aprobacion'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/solicitudes/', views.VerSolicitudes.as_view(),
         name='solicitudes'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/solicitudes/<int:id_solicitud>', views.DetalleSolicitud.as_view(),
         name='detalle_solicitud'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/solicitudes/<int:id_solicitud>/aprobar/', views.AprobarSolicitudDeUS.as_view(),
         name='aprobar_solicitud'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/solicitudes/<int:id_solicitud>/rechazar/', views.RechazarSolicitudDeUS.as_view(),
         name='rechazar_solicitud'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/asignar_dev/', views.AsignarDevAUserStory.as_view(), name='asignar_dev_US'),
    path('<int:id_proyecto>/backlog/US/<int:id_us>/cambiar_estado/', views.CambiarEstadoUSView.as_view(), name='cambiar_estado_us'),
    path('<int:id_proyecto>/equipo/<int:id_equipo>/', views.DetalleEquipoView.as_view(), name='ver_equipo'),
    path('<int:id_proyecto>/equipo/<int:id_equipo>/editar/', views.ActualizarEquipoView.as_view(), name='editar_equipo'),
    path('<int:id_proyecto>/equipo/<int:id_equipo>/asignar_roles/<int:id_usuario>', views.AsignarRolProyectoAUsuario.as_view(), name='asignar_rol_proyecto'),
    path('<int:id_proyecto>/sprint/', views.VerSprintsView.as_view(), name='ver_sprints'),
    path('<int:id_proyecto>/sprint/crear/', views.CrearSprint.as_view(), name='crear_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/editar/', views.ActualizarSprintView.as_view(), name='editar_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/', views.DetalleSprintView.as_view(), name='ver_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/asignar_miembro/', views.AsignarMiembroASprint.as_view(), name='asignar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/editar_miembro/<int:id_miembrosprint>',
         views.ActualizarMiembrosSprintView.as_view(), name='actualizar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/eliminar_miembro/<int:id_miembrosprint>',
         views.BorrarMiembrosSprintView.as_view(), name='eliminar_miembros_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/asignar_us/', views.AsignarUSASprint.as_view(), name='asignar_us_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/eliminar_us/<int:id_us>/', views.BorrarUSASprint.as_view(), name='eliminar_us_sprint'),
    path('<int:id_proyecto>/sprint/<int:id_sprint>/iniciar/', views.IniciarSprint.as_view(), name='iniciar_sprint'),
    path('<int:id_proyecto>/backlog/', views.verProductBacklog.as_view(), name='ver_product_backlog'),
    path('<int:id_proyecto>/kanban/', views.TableroKanbanView.as_view(), name='kanban'),

]

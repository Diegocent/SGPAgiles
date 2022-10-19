from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from Usuario.models import Usuario, RolSistema, Permisos


"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **login** - Funcion para hacer el login 
"""
# === login ===

def login(request):
        if not request.user.is_authenticated:
                return render(request, 'index.html')
        else:
                cantidad_de_usuarios = Usuario.objects.count()
                unico_usuario_es_admin = request.user.es_admin()
                #si hay un solo usuario y el current usuario no es admin, se le asigna como admin
                if(cantidad_de_usuarios == 1 and not unico_usuario_es_admin):
                        array_de_roles = RolSistema.objects.all().filter(nombre="admin")
                        if len(array_de_roles) == 0: #si no existe el rol de admin, se crea
                                permisos = [
                                        Permisos(nombre="Ver Permiso", descripcion="Permiso para Ver Permisos"),
                                        Permisos(nombre="Crear Permiso", descripcion="Permiso para Crear Permisos"),
                                        Permisos(nombre="Editar Permiso", descripcion="Permiso para Editar Permisos"),
                                        Permisos(nombre="Borrar Permiso", descripcion="Permiso para Borrar Permisos"),
                                        Permisos(nombre="Ver RolSistema",
                                                descripcion="Permiso para Ver Roles de Sistema"),
                                        Permisos(nombre="Crear RolSistema",
                                                descripcion="Permiso para Crear Roles de Sistema"),
                                        Permisos(nombre="Editar RolSistema",
                                                descripcion="Permiso para Editar Roles de Sistema"),
                                        Permisos(nombre="Borrar RolSistema",
                                                descripcion="Permiso para Borrar Roles de Sistema"),
                                        Permisos(nombre="Ver RolProyecto",
                                                descripcion="Permiso para Ver Roles de Proyecto"),
                                        Permisos(nombre="Crear RolProyecto",
                                                descripcion="Permiso para Crear Roles de Proyecto"),
                                        Permisos(nombre="Editar RolProyecto",
                                                descripcion="Permiso para Editar Roles de Proyecto"),
                                        Permisos(nombre="Borrar RolProyecto",
                                                descripcion="Permiso para Borrar Roles de Proyecto"),
                                        Permisos(nombre="Ver Usuario", descripcion="Permiso para Ver Usuarios"),
                                        Permisos(nombre="Crear Usuario", descripcion="Permiso para Crear Usuarios"),
                                        Permisos(nombre="Editar Usuario", descripcion="Permiso para Editar Usuarios"),
                                        Permisos(nombre="Borrar Usuario", descripcion="Permiso para Borrar Usuarios"),
                                        Permisos(nombre="Ver Equipo", descripcion="Permiso para Ver Equipo"),
                                        Permisos(nombre="Crear Equipo", descripcion="Permiso para Crear Equipo"),
                                        Permisos(nombre="Editar Equipo", descripcion="Permiso para Editar Equipo"),
                                        Permisos(nombre="Borrar Equipo", descripcion="Permiso para Borrar Equipo"),
                                        Permisos(nombre="Ver Proyecto", descripcion="Permiso para Ver Proyecto"),
                                        Permisos(nombre="Crear Proyecto", descripcion="Permiso para Crear Proyecto"),
                                        Permisos(nombre="Editar Proyecto", descripcion="Permiso para Editar Proyecto"),
                                        Permisos(nombre="Borrar Proyecto", descripcion="Permiso para Borrar Proyecto"),
                                        Permisos(nombre="Iniciar Proyecto", descripcion="Permiso para Iniciar Proyecto"),
                                        Permisos(nombre="Cancelar Proyecto",
                                                descripcion="Permiso para Cancelar Proyecto"),
                                        Permisos(nombre="Ver Sprint", descripcion="Permiso para Ver Sprint"),
                                        Permisos(nombre="Crear Sprint", descripcion="Permiso para Crear Sprint"),
                                        Permisos(nombre="Editar Sprint", descripcion="Permiso para Editar Sprint"),
                                        Permisos(nombre="Borrar Sprint", descripcion="Permiso para Borrar Sprint"),
                                        Permisos(nombre="Iniciar Sprint", descripcion="Permiso para Iniciar Sprint"),
                                        Permisos(nombre="Cancelar Sprint", descripcion="Permiso para Cancelar Sprint"),
                                        Permisos(nombre="Ver TipoUserStory",
                                                descripcion="Permiso para Ver Tipos de User Story"),
                                        Permisos(nombre="Crear TipoUserStory",
                                                descripcion="Permiso para Crear Tipos de User Story"),
                                        Permisos(nombre="Editar TipoUserStory",
                                                descripcion="Permiso para Editar Tipos de User Story"),
                                        Permisos(nombre="Borrar TipoUserStory",
                                                descripcion="Permiso para Borrar Tipos de User Story"),
                                        Permisos(nombre="Ver EstadoUS",
                                                descripcion="Permiso para Ver Estados de User Story"),
                                        Permisos(nombre="Crear EstadoUS",
                                                descripcion="Permiso para Crear Estados de User Story"),
                                        Permisos(nombre="Editar EstadoUS",
                                                descripcion="Permiso para Editar Estados de User Story"),
                                        Permisos(nombre="Borrar EstadoUS",
                                                descripcion="Permiso para Borrar Estados de User Story"),
                                        Permisos(nombre="Cambiar EstadoUS",
                                                descripcion="Permiso para Cambiar Estados de User Story"),
                                        Permisos(nombre="Ver UserStory", descripcion="Permiso para Ver User Story"),
                                        Permisos(nombre="Crear UserStory", descripcion="Permiso para Crear User Story"),
                                        Permisos(nombre="Editar UserStory",
                                                descripcion="Permiso para Editar User Story"),
                                        Permisos(nombre="Borrar UserStory",
                                                descripcion="Permiso para Borrar User Story"),
                                ]
                                Permisos.objects.bulk_create(permisos)
                                permiso_de_admin = Permisos.objects.create(nombre="Permiso de administrador", descripcion="Permiso para administrador de sistema.")
                                admin = RolSistema.objects.create(nombre="admin", descripcion="Administrador del sistema.")
                                admin.permisos.add(permiso_de_admin)
                                admin.permisos.add(*permisos)

                                request.user.rolSistema.add(admin)
                        else: #si existe el rol de admin, se le asigna directamente al usuario
                                admin = RolSistema.objects.get(nombre="admin")
                                request.user.rolSistema.add(admin)
                return render(request, 'index.html')






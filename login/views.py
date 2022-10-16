from django.http import HttpResponse
from django.shortcuts import render
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
                                permiso_de_admin = Permisos.objects.create(nombre="Permiso de administrador", descripcion="Permiso para administrador de sistema.")
                                admin = RolSistema.objects.create(nombre="admin", descripcion="Administrador del sistema.")
                                admin.permisos.add(permiso_de_admin)
                                request.user.rolSistema.add(admin)
                        else: #si existe el rol de admin, se le asigna directamente al usuario
                                admin = RolSistema.objects.get(nombre="admin")
                                request.user.rolSistema.add(admin)
                return render(request, 'index.html')






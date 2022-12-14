from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .forms import FormRolSistema, FormCrearPermisos, FormAsignarRol
from .models import RolProyecto, RolSistema, Permisos, Usuario
from django.core.exceptions import ObjectDoesNotExist

"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **CrearRolSistemaView** - Se crean los roles del sistema (salta a la seccion [[views.py#CrearRolSistemaView]])
2. **CrearPermisoView** - Se crean los permisos del proyecto (salta a la seccion [[views.py#CrearPermisoView]])
3. **AsignarRolSistemaView** - Se asignan los roles al sistema (salta a la seccion [[views.py#AsignarRolSistemaView]])
4. **VerRolesSistemaView** - Se podra visualizar los roles asignados al sistema (salta a la seccion [[views.py#VerRolesSistemaView]])
5. **VerPermisosView** - Se podra visualizar los Permisos (salta a la seccion [[views.py#VerPermisosView]])
6. **VerConfigView** - Se podra ver la configuracion a seguir (salta a la seccion [[views.py#VerConfigView]])
7. **VerUsuariosConRolesView** - Se podra visualizar la lista con los usuarios y 
    los respectivos roles que le fueron asignados (salta a la seccion [[views.py#VerUsuariosConRolesView]])
"""


class CrearPermisoView(View):
    form_class = FormCrearPermisos
    permisos = ["Crear Permiso"]

    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'roles/crear_permisos.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Permisos.objects.create(
                nombre=cleaned_data["nombre"],
                descripcion=cleaned_data["descripcion"],
            )
            messages.success(request, 'Creado exitosamente!')
            return redirect('ver_permisos')
        return render(request, 'roles/crear_permisos.html', {'form': form})


class CrearRolSistemaView(View):
    form_class = FormRolSistema
    permisos = ["Crear RolSistema"]

    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'roles/crear_roles.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            rol_del_post = form.cleaned_data
            array_de_roles = RolSistema.objects.all().filter(nombre=rol_del_post['nombre'])
            if len(array_de_roles) == 0:
                rol = RolSistema.objects.create(nombre=rol_del_post['nombre'], descripcion=rol_del_post['descripcion'])

                for permisos in rol_del_post['permisos']:
                    rol.permisos.add(permisos)
                rol.save()
                messages.success(request, 'Creado exitosamente!')
            else:
                messages.error(request, "Ya existe un rol con ese nombre")

            return redirect('ver_roles_sistema')
        return render(request, 'roles/crear_roles.html', {'form': form})


class EditarRolSistemaView(View):
    form_class = FormRolSistema
    permisos = ["Crear RolSistema"]

    def get(self, request, id_rol):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                try:
                    rol = RolSistema.objects.get(id=id_rol)
                except ObjectDoesNotExist:
                    messages.error(request, "No se encuentra al rol con esas caracteristicas")
                    return redirect("ver_config")
                form = self.form_class(instance=rol)
                return render(request, 'roles/crear_roles.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_rol):
        rol = RolSistema.objects.get(id=id_rol)
        form = self.form_class(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('ver_roles_sistema')
        return render(request, 'roles/crear_roles.html', {'form': form})


class AsignarRolSistemaView(View):
    form_class = FormAsignarRol
    permisos = ["Asignar RolSistema"]
    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'roles/asignar_rol.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario: Usuario = cleaned_data["usuario"]
            roles = cleaned_data["rol"]
            for rol in roles:
                usuario.rolSistema.add(rol)
            usuario.save()
            messages.success(request, 'Creado exitosamente!')

            return redirect('usuarios_con_roles')
        return render(request, 'roles/asignar_rol.html', {'form': form})


class VerConfigView(View):
    def get(self, request):
        usuario: Usuario = request.user
        if usuario.is_authenticated:
            if usuario.es_admin():
                context = {
                    'admin': True,
                }
            else:
                context = {
                    "admin": False,
                }
            return render(request, 'ver_config.html', context)
        else:
            return redirect("home")


class VerRolesSistemaView(View):
    permisos = ["Ver RolSistema"]
    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                roles = RolSistema.objects.all()
                context = {
                        'crear_rol': True,
                        'roles': roles
                }
                return render(request, 'roles/ver_roles_sistema.html', context)
            elif not tiene_permisos:
                 return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class VerPermisosView(View):
    permisos = ["Ver Permiso"]
    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                permisos = Permisos.objects.all()
                context = {
                        'crear_permiso': True,
                        'permisos': permisos
                }
                return render(request, 'roles/ver_permisos.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class VerUsuariosConRolesView(View):
    permisos = ["Ser Administrador"]
    def get(self, request):
        usuario: Usuario = request.user
        if usuario.is_authenticated:
            if usuario.es_admin():
                usuarios = Usuario.objects.all()

                context = {
                        'usuarios': usuarios
                }
                return render(request, 'roles/ver_usuarios_con_roles.html', context)
            else:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not usuario.is_authenticated:
            return redirect("home")
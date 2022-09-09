from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import FormRolSistema, FormRolProyecto, FormCrearPermisos, FormAsignarRol
from .models import RolProyecto, RolSistema, Permisos, Usuario

"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **crear_rol_sistema** - Se crean los roles del sistema (salta a la seccion [[views.py#crear_rol_sistema]])
2. **CrearPermisoView** - Se crean los permisos del proyecto (salta a la seccion [[views.py#CrearPermisoView]])
3. **AsignarRolSistemaView** - Se asignan los roles al sistema (salta a la seccion [[views.py#AsignarRolSistemaView]])
"""

def crear_rol_sistema(request):
    rol_creado = False
    mensaje_error = ""
    if request.method == "POST":
        post_request = FormRolSistema(request.POST)
        if post_request.is_valid():
            rol_del_post = post_request.cleaned_data
            array_de_roles = RolSistema.objects.all().filter(name=rol_del_post['name_role'])
            if len(array_de_roles) == 0:
                rol = RolSistema(nombre=rol_del_post['name_role'], descripcion=rol_del_post['description_role'])
                rol.save()

                for permisos in rol_del_post['permissions']:
                    rol.permisos.add(permisos)

                rol_creado=True
            else:
                mensaje_error = "Ya existe un rol con el mismo nombre."

    form = FormRolSistema()
    return render(request, 'crear_rol_sistema.html', {'form': form, 'rol_creado': rol_creado,
                                                      "mensaje_error": mensaje_error})


class CrearPermisoView(View, LoginRequiredMixin):
    form_class = FormCrearPermisos

    def get(self, request):
        form = self.form_class()
        return render(request, 'roles/crear_permisos.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Permisos.objects.create(
                nombre=cleaned_data["nombre"],
                descripcion=cleaned_data["descripcion"],
            )
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('crear_permiso')
        return render(request, 'roles/crear_permisos.html', {'form': form})


class CrearRolSistemaView(View, LoginRequiredMixin):
    form_class = FormRolSistema

    def get(self, request):
        form = self.form_class()
        return render(request, 'roles/crear_roles.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            rol_del_post = form.cleaned_data
            array_de_roles = RolSistema.objects.all().filter(nombre=rol_del_post['nombre'])
            if len(array_de_roles) == 0:
                rol = RolSistema.objects.create(nombre=rol_del_post['nombre'], descripcion=rol_del_post['descripcion'])

                for permisos in rol_del_post['permisos']:
                    rol.permisos.add(permisos)
                messages.success(request, 'Creado exitosamente!')
            else:
                messages.error(request="Ya existe un rol con ese nombre")

            return HttpResponseRedirect('crear_roles')
        return render(request, 'roles/crear_roles.html', {'form': form})


class AsignarRolSistemaView(View, LoginRequiredMixin):
    form_class = FormAsignarRol

    def get(self, request):
        form = self.form_class()
        return render(request, 'roles/asignar_rol.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario: Usuario = cleaned_data["usuario"]
            roles: RolSistema = cleaned_data["rol"]
            for rol in roles:
                usuario.rolSistema.add(rol)
            messages.success(request, 'Creado exitosamente!')

            return HttpResponseRedirect('asignar_rol')
        return render(request, 'roles/asignar_rol.html', {'form': form})

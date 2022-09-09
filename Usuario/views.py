from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import FormRolSistema, FormCrearPermisos, FormAsignarRol
from .models import RolProyecto, RolSistema, Permisos, Usuario

"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **CrearRolSistemaView** - Se crean los roles del sistema (salta a la seccion [[views.py#CrearRolSistemaView]])
2. **CrearPermisoView** - Se crean los permisos del proyecto (salta a la seccion [[views.py#CrearPermisoView]])
3. **AsignarRolSistemaView** - Se asignan los roles al sistema (salta a la seccion [[views.py#AsignarRolSistemaView]])
"""


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
                rol.save()
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
            roles = cleaned_data["rol"]
            for rol in roles:
                usuario.rolSistema.add(rol)
            usuario.save()
            messages.success(request, 'Creado exitosamente!')

            return HttpResponseRedirect('asignar_rol')
        return render(request, 'roles/asignar_rol.html', {'form': form})

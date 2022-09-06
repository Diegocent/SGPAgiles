from django.shortcuts import render

from .forms import FormRolSistema, FormRolProyecto
from .models import RolProyecto, RolSistema


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


def crear_rol_proyecto(request):
    rol_creado = False
    mensaje_error = ""
    if request.method == "POST":
        post_request = FormRolProyecto(request.POST)
        if post_request.is_valid():
            rol_del_post = post_request.cleaned_data
            array_de_roles = RolProyecto.objects.all().filter(name=rol_del_post['name_role'])
            if len(array_de_roles) == 0:
                rol = RolProyecto(nombre=rol_del_post['name_role'], descripcion=rol_del_post['description_role'])
                rol.save()

                for permisos in rol_del_post['permissions']:
                    rol.permisos.add(permisos)

                rol_creado = True
            else:
                mensaje_error = "Ya existe un rol con el mismo nombre."

    form = FormRolProyecto()
    # formRol.fields['permissions'].choices=CHOICES #agregamos los permisos al form
    # enviamos el form vacio y el numero que indica si se cargo un rol o no
    return render(request, 'crear_rol_proyecto.html',
                  {'form': form, 'rol_creado': rol_creado, "mensaje_error": mensaje_error})

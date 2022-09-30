from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FormCrearProyecto, FormCrearEquipo, FormIniciarProyecto, FormRolProyecto, FormTiposUS, FormEstadoUS, \
    FormUS, FormSprint
from .models import Proyecto, EstadoProyecto, Equipo, TipoUserStory, UserStory, EstadoUS, Sprint
from Usuario.models import Usuario, RolProyecto
from django.contrib import messages
from datetime import date
# Create your views here.
"""
Todos los vgikiews para SGPAgiles 
Actualmente contamos con los siguientes views en Proyecto:

1. **CrearProyectoView** - Vista para crear Proyectos (salta a la seccion [[views.py#CrearProyectoView]])
2. **CrearEquipoView** - Se crea la vista para Equipo (salta a la seccion [[views.py#CrearEquipoView]])
3. **VerProyectoView** - Vista para visualizar detalle de un proyecto (salta a la seccion [[views.py#VerProyectoView]])
4. **VerProyectosView** - Vista para visualizar listado de los Proyectos (salta a la seccion [[views.py#VerProyectosView]])
5. **IniciarProyecto** - Vista para iniciar proyecto (salta a la seccion [[views.py#IniciarProyectoView]])
6. **CrearRolProyectoView** - Vista para crear los roles del proyecto (salta a la seccion [[views.py#CrearRolProyectoView]])
7. **VerRolesProyectoView** - Se podra visualizar los roles asignados al proyecto (salta a la seccion [[views.py#VerRolesProyectoView]])
"""


class VerProyectosView(View, LoginRequiredMixin):

    def get(self, request):
        usuario: Usuario = request.user
        if usuario.is_authenticated:
            if usuario.es_admin():
                proyectos = Proyecto.objects.all()
                context = {
                    'admin': True,
                    'proyectos': proyectos
                }
            else:
                context = {
                    "admin": False,
                    "proyectos": []
                }
                equipos = Equipo.objects.all().filter(miembros__id=usuario.id)
                for equipo in equipos:
                    proyecto = Proyecto.objects.get(equipo=equipo)
                    context['proyectos'].append(proyecto)
            return render(request, 'ver_proyectos.html', context)
        else:
            return render(request, 'account/login.html')


class CrearProyectoView(View, LoginRequiredMixin):
    form_class = FormCrearProyecto

    def get(self, request):
        if not request.user.es_admin():
           return HttpResponseRedirect('/')
        form = self.form_class()
        return render(request, 'crear_proyecto.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            proyecto = Proyecto.objects.create(
                nombre=cleaned_data["nombre"],
                descripcion=cleaned_data["descripcion"],
                estado=EstadoProyecto.NO_INICIADO
            )
            scrum = RolProyecto.objects.create(nombre="scrum master",
                                       descripcion="Scrum Master del Proyecto.",
                                       proyecto=proyecto)
            RolProyecto.objects.create(nombre="Developer",
                                       descripcion="Developer del Proyecto.",
                                       proyecto=proyecto)
            usuario: Usuario = cleaned_data["scrum_master"]
            usuario.rolProyecto.add(scrum)
            usuario.save()
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('/proyecto')
        return render(request, 'crear_proyecto.html', {'form': form})


class VerProyectoView(View, LoginRequiredMixin):

        def verificar_estados(self, tipos):
            ok = True
            for tipo in tipos:
                estado = EstadoUS.objects.all().filter(tipoUserStory=tipo)
                if len(estado) == 0:
                    ok = False
            return ok

        def get(self, request, id_proyecto):
            usuario: Usuario = request.user
            p = Proyecto.objects.get(id=id_proyecto)
            tipos = TipoUserStory.objects.all().filter(proyecto=p)

            us = UserStory.objects.all().filter(proyecto=p)
            equipo = p.equipo
            todos_con_estados = self.verificar_estados(tipos)
            if equipo:
                miembros = equipo.miembros.all()

                if usuario not in miembros and not usuario.es_admin() and not usuario.es_scrum_master(id_proyecto):
                    messages.warning(request, "No puedes ver este proyecto.")
                    return HttpResponseRedirect('ver_proyectos')

                context = {
                    "proyecto": p,
                    "equipo": equipo,
                    "miembros": miembros,
                    "tipos": tipos,
                    "todos_con_estados": todos_con_estados,
                    "us":us
                }
            else:
                if not usuario.es_admin():
                    messages.warning(request, "No puedes ver este proyecto.")
                    return HttpResponseRedirect('ver_proyectos')
                context = {
                    "proyecto": p,
                    "equipo": equipo,
                    "tipos": tipos,
                    "todos_con_estados": todos_con_estados,
                    "us": us
                }
            return render(request, 'detalle_proyecto.html', context)


class CrearEquipoView(View, LoginRequiredMixin):
    form_class = FormCrearEquipo

    def get(self, request, id_proyecto):
        if not request.user.es_admin():
            return HttpResponseRedirect('/')
        form = self.form_class()
        return render(request, 'crear_equipo.html', {'form': form})

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            equipo = Equipo.objects.create(
                nombre=cleaned_data["nombre"],
            )
            for miembro in cleaned_data["miembros"]:
                equipo.miembros.add(miembro)
            proyecto = Proyecto.objects.get(id=id_proyecto)
            print(equipo)
            proyecto.equipo = equipo
            proyecto.save()
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('.')
        return render(request, 'crear_proyecto.html', {'form': form})


class IniciarProyectoView(View, LoginRequiredMixin):
    form_class = FormIniciarProyecto

    def get(self, request, id_proyecto):
        if not request.user.es_admin():
            return HttpResponseRedirect('/')
        form = self.form_class()
        return render(request, 'iniciar_proyecto.html', {'form': form})

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            proyecto = Proyecto.objects.get(id=id_proyecto)
            proyecto.fecha_fin_estimada = cleaned_data["fecha_fin_estimada"]
            proyecto.fecha_inicio = date.today()
            proyecto.estado = EstadoProyecto.EN_PROCESO
            proyecto.save()
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('.')
        return render(request, 'iniciar_proyecto.html', {'form': form})


class CrearRolProyectoView(View, LoginRequiredMixin):
    form_class = FormRolProyecto

    def get(self, request, id_proyecto):
        form = self.form_class()
        return render(request, 'roles/crear_rol_proyecto.html', {'form': form})

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            rol_del_post = form.cleaned_data
            array_de_roles = RolProyecto.objects.all().filter(nombre=rol_del_post['nombre'])
            if len(array_de_roles) == 0:
                rol = RolProyecto.objects.create(nombre=rol_del_post['nombre'], descripcion=rol_del_post['descripcion']
                                                 , proyecto_id=id_proyecto)

                for permisos in rol_del_post['permisos']:
                    rol.permisos.add(permisos)
                rol.save()
                messages.success(request, 'Creado exitosamente!')
            else:
                messages.error(request="Ya existe un rol con ese nombre")

            return HttpResponseRedirect('ver_roles')
        return render(request, 'roles/crear_rol_proyecto.html', {'form': form})


class VerRolesProyectoView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto):
        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            roles = RolProyecto.objects.all().filter(proyecto=id_proyecto)
            context = {
                'crear_rol': True,
                'roles': roles
            }
        else:
            context = {
                'crear_rol': False,
                "roles": []
            }
        return render(request, 'roles/ver_roles.html', context)


class VerTiposdeUSView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            tipos = TipoUserStory.objects.all().filter(proyecto=id_proyecto)
            context = {
                'crear_tipoUS': True,
                'tipos': tipos,
                "id_proyecto": id_proyecto
            }
        else:
            context = {
                'crear_tipoUS': False,
                "tipos": [],
                "id_proyecto": id_proyecto
            }
        return render(request, 'tipoUS/ver_tiposUS.html', context)


class CrearTiposUSView(View, LoginRequiredMixin):
    form_class = FormTiposUS

    def get(self, request, id_proyecto):
        form = self.form_class()
        return render(request, 'tipoUS/creartipous.html', {'form': form})

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            tipo_del_post = form.cleaned_data
            array_de_tipos = TipoUserStory.objects.all().filter(nombre=tipo_del_post['nombre'], proyecto_id=id_proyecto) | TipoUserStory.objects.\
                all().filter(nombre=tipo_del_post['prefijo'], proyecto_id=id_proyecto)

            if len(array_de_tipos) == 0:
                TipoUserStory.objects.create(nombre=tipo_del_post['nombre'], prefijo=tipo_del_post['prefijo']
                                                 , proyecto_id=id_proyecto)

                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'tipoUS/creartipous.html', {'form': form})
            return HttpResponseRedirect('ver_tipoUS', messages)
        return render(request, 'tipoUS/creartipous.html', {'form': form})


class DetalleTiposUSView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto, id_tipous):
        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            tipo = TipoUserStory.objects.get(id= id_tipous)
            estados = EstadoUS.objects.all().filter(tipoUserStory_id=id_tipous)
            context = {
                'tipo': tipo,
                'estados': estados,
                'id_proyecto': id_proyecto,
                'id_tipous': id_tipous
            }
            return render(request, 'tipoUS/detalle_tipoUS.html', context)
        else:
            return render(request, '/')


class CrearEstadosUSView(View, LoginRequiredMixin):
    form_class = FormEstadoUS

    def get(self, request, id_proyecto, id_tipous):
        form = self.form_class()
        default = request.GET["default"]
        if default == 'true':
            tipo = TipoUserStory.objects.get(id=id_tipous)
            EstadoUS.objects.create(nombre="TO DO", tipoUserStory=tipo)
            EstadoUS.objects.create(nombre="DOING", tipoUserStory=tipo)
            EstadoUS.objects.create(nombre="DONE", tipoUserStory=tipo)
            return HttpResponseRedirect('/proyecto/{}/tipoUS/{}'.format(id_proyecto, id_tipous))
        elif default == 'false':
            return render(request, 'tipoUS/crearestadous.html', {'form': form})

    def post(self, request, id_proyecto, id_tipous):
        form = self.form_class(request.POST)
        if form.is_valid():
            estado_del_post = form.cleaned_data
            array_de_estados = EstadoUS.objects.all().filter(nombre=estado_del_post['nombre'], tipoUserStory_id=id_tipous)

            if len(array_de_estados) == 0:
                tipo = TipoUserStory.objects.get(id=id_tipous)
                EstadoUS.objects.create(nombre=estado_del_post['nombre'], tipoUserStory=tipo)

                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'tipoUS/crearestadous.html', {'form': form})
            return HttpResponseRedirect('/proyecto/{}/tipoUS/{}'.format(id_proyecto, id_tipous))
        return render(request, 'tipoUS/crearestadous.html', {'form': form})


class CrearUSView(View, LoginRequiredMixin):
    form_class = FormUS

    def get(self, request, id_proyecto):
        form = self.form_class()
        form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
        return render(request, 'US/crearus.html', {'form': form})

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            us = form.cleaned_data
            array_de_us = UserStory.objects.all().filter(nombre=us['nombre'], proyecto_id=id_proyecto)

            if len(array_de_us) == 0:
                p = Proyecto.objects.get(id=id_proyecto)
                UserStory.objects.create(nombre=us['nombre'], descripcion=us['descripcion'], proyecto_id=id_proyecto,
                                         tipo=us['tipo'])

                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'US/crearus.html', {'form': form})
            return HttpResponseRedirect('/proyecto/{}/US'.format(id_proyecto))
        return render(request, 'US/crearus.html', {'form': form})


class VerUSView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto):
        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            uss = UserStory.objects.all().filter(proyecto=id_proyecto)
            context = {
                'uss': uss,
                'id_proyecto' : id_proyecto
            }
        else:
            context = {
                "uss": [],
                'id_proyecto': id_proyecto
            }
        return render(request, 'US/ver_US.html', context)


class ActualizarUSView(View, LoginRequiredMixin):
    form_class = FormUS

    def get(self, request, id_proyecto, id_us):
        us = UserStory.objects.get(id=id_us)
        form = FormUS(instance=us)
        form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
        return render(request, 'US/editarus.html', {'form': form})

    def post(self, request, id_proyecto, id_us):
        us = UserStory.objects.get(id=id_us)
        form = FormUS(request.POST, instance=us)
        if form.is_valid():
            us = form.cleaned_data
            array_de_us = UserStory.objects.all().filter(nombre=us['nombre'], proyecto_id=id_proyecto)

            if len(array_de_us) == 0:
                form.save()

                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'US/editarus.html', {'form': form})
            return HttpResponseRedirect('/proyecto/{}/US'.format(id_proyecto))
        return render(request, 'US/editarus.html', {'form': form})


class BorrarUSView(View, LoginRequiredMixin):
    form_class = FormUS

    def get(self, request, id_proyecto, id_us):
        us = UserStory.objects.get(id=id_us)
        form = FormUS(instance=us)
        return render(request, 'US/borrarus.html', {'form': form})

    def post(self, request, id_proyecto, id_us):
        us = UserStory.objects.get(id=id_us)

        us.delete()

        return HttpResponseRedirect('/proyecto/{}/US'.format(id_proyecto))


class DetalleEquipoView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto, id_equipo):
        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            equipo = Equipo.objects.get(id=id_equipo)

            miembros = equipo.miembros.all()

            miembrosroles = []
            for miembro in miembros:
                rol = miembro.rolProyecto.filter(proyecto_id=id_proyecto)
                dicc = {"miembro": miembro, "rol": rol}
                miembrosroles.append(dicc)
            context = {
                'equipo': equipo,
                'miembrosroles': miembrosroles,
                'id_proyecto': id_proyecto,
            }
            return render(request, 'equipo/detalle_equipo.html', context)
        else:
            return render(request, '/')


class ActualizarEquipoView(View, LoginRequiredMixin):

    def get(self, request, id_proyecto, id_equipo):
        equipo = Equipo.objects.get(id=id_equipo)
        form = FormCrearEquipo(instance=equipo)
        return render(request, 'equipo/editarequipo.html', {'form': form})

    def post(self, request, id_proyecto, id_equipo):
        equipo = Equipo.objects.get(id=id_equipo)
        form = FormCrearEquipo(request.POST, instance=equipo)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/proyecto/{}/equipo/{}'.format(id_proyecto, id_equipo))
        return render(request, 'US/editarus.html', {'form': form})


class CrearSprint(View, LoginRequiredMixin):
    form_class = FormSprint

    def get(self, request, id_proyecto):
        sprints = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoProyecto.EN_PROCESO)
        if len(sprints) == 0:
            form = self.form_class()
            form.fields['product_backlog'].queryset = UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id__isnull=True)
            return render(request, 'sprint/crearsprint.html', {'form': form})
        else:
            return render(request, 'sprint/warning.html',)

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            sprintform = form.cleaned_data
            array_de_sprint = Sprint.objects.all().filter(numero=sprintform['numero'], proyecto_id=id_proyecto)

            if len(array_de_sprint) == 0:
                p = Proyecto.objects.get(id=id_proyecto)
                sprint = Sprint.objects.create(numero=sprintform['numero'], descripcion=sprintform['descripcion'],
                                             proyecto_id=id_proyecto, fecha_fin=sprintform["fecha_fin"],
                                             fecha_inicio=date.today(), estado=EstadoProyecto.EN_PROCESO)

                user_stories = sprintform["product_backlog"]
                for us in user_stories:
                    us.sprint_id = sprint.id
                    us.save()
            else:
                return render(request, 'sprint/crearsprint.html', {'form': form})
            return HttpResponseRedirect('/proyecto/{}'.format(id_proyecto))
        return render(request, 'sprint/crearsprint.html', {'form': form})
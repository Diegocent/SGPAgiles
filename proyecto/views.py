
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FormCrearProyecto, FormCrearEquipo, FormIniciarProyecto, FormRolProyecto, FormTiposUS, FormEstadoUS, \
    FormUS, FormSprint
from .models import Proyecto, EstadoProyecto, Equipo, TipoUserStory, UserStory, EstadoUS, Sprint, OrdenEstado, \
    EstadoSprint
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
8. **CrearSprint** Vista para crear los Sprints (salta a la seccion [[views.py#CrearSprint]])
9. **DetalleSprintView** - Se podran visualizar los Sprints del proyecto (salta a la seccion [[views.py#DetalleSprintView]])
10. **ActualizarEquipoView** - Vista para actualizar/modificar los datos del Equipo (salta a la seccion [[views.py#ActualizarEquipoView]])
11. **DetalleEquipoView** - Se podra visualizar los detalles del equipo (salta a la seccion [[views.py#DetalleEquipoView]])
12. **CrearTiposUSView** - Vista para crear los Tipos de US (salta a la seccion [[views.py#CrearTipoUSView]])
13. **VerTiposdeUSView** - Se visualiza los tipos de US (salta a la seccion [[views.py#VerTiposUSView]])
14. **DetalleTiposUSView** - Se podra visualizar los detalles del Tipo de US (salta a la seccion [[views.py#DetalleTiposUSView]])
15. **CrearEstadosUSView** - Vista para crear los estados del US (salta a la seccion [[views.py#CrearEstadoUSView]])
16. **CrearUSView** - Vista para crear un US (salta a la seccion [[views.py#CrearUSView]])
17. **VerUSView** - Vista para visualizar los US existentes (salta a la seccion [[views.py#VerUSView]])
18. **BorrarUSView** - Vista para eliminar un US (salta a la seccion [[views.py#BorrarUSView]])
19. **ActualizarUSView** - Vista para actualizar/modificar los datos del Equipo (salta a la seccion [[views.py#ActualizarUSView]])
20. ** verProductBacklog** - Vista para el Product Backlog (salta a la seccion [[views.py# verProductBacklog]])
"""


class VerProyectosView(View):

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


class CrearProyectoView(View):
    permisos = ["Crear Proyecto"]
    form_class = FormCrearProyecto

    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'crear_proyecto.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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

            equipo = Equipo.objects.create(nombre = "")
            equipo.miembros.add(usuario)

            proyecto.equipo = equipo
            proyecto.save()

            messages.success(request, 'Creado exitosamente!')
            return redirect('ver_proyectos')
        return render(request, 'crear_proyecto.html', {'form': form})


class VerProyectoView(View):
    permisos = ["Ver Proyecto"]
    def verificar_estados(self, tipos):
        ok = True
        for tipo in tipos:
            estado = EstadoUS.objects.all().filter(tipoUserStory=tipo)
            if len(estado) == 0:
                ok = False
        return ok

    def get(self, request, id_proyecto):
        usuario: Usuario = request.user
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                p = Proyecto.objects.get(id=id_proyecto)
                tipos = TipoUserStory.objects.all().filter(proyecto=p)


                sprint = Sprint.objects.all().filter(proyecto_id=id_proyecto, estado=EstadoProyecto.EN_PROCESO)


                us = UserStory.objects.all().filter(proyecto=p)
                equipo = p.equipo
                todos_con_estados = self.verificar_estados(tipos)
                if equipo:
                    miembros = equipo.miembros.all()

                    if usuario not in miembros and not usuario.es_admin() and not usuario.es_scrum_master(id_proyecto):
                        messages.warning(request, "No puedes ver este proyecto.")
                        return redirect('ver_proyectos')

                    context = {
                        "proyecto": p,
                        "sprint": sprint,
                        "equipo": equipo,
                        "miembros": miembros,
                        "tipos": tipos,
                        "todos_con_estados": todos_con_estados,
                        "us":us,
                        "id_proyecto": id_proyecto
                    }
                else:
                    if not usuario.es_admin():
                        messages.warning(request, "No puedes ver este proyecto.")
                        return redirect('ver_proyectos')
                    context = {
                        "proyecto": p,
                        "equipo": equipo,
                        "tipos": tipos,
                        "todos_con_estados": todos_con_estados,
                        "us": us,
                        "id_proyecto":id_proyecto
                    }
                return render(request, 'detalle_proyecto.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class CrearEquipoView(View):
    permisos = ["Crear Equipo"]
    form_class = FormCrearEquipo

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'crear_equipo.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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
            return redirect('detalle_proyecto', id_proyecto)
        return render(request, 'crear_proyecto.html', {'form': form})


class IniciarProyectoView(View):
    form_class = FormIniciarProyecto
    permisos = ["Iniciar Proyecto"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'iniciar_proyecto.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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
            return redirect('detalle_proyecto', id_proyecto)
        return render(request, 'iniciar_proyecto.html', {'form': form})


class CrearRolProyectoView(View):
    form_class = FormRolProyecto
    permisos = ["Crear RolProyecto"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'roles/crear_rol_proyecto.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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

            return redirect('ver_roles', id_proyecto)
        return render(request, 'roles/crear_rol_proyecto.html', {'form': form})


class VerRolesProyectoView(View):
    permisos = ["Ver RolProyecto"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                roles = RolProyecto.objects.all().filter(proyecto=id_proyecto)
                context = {
                    'crear_rol': True,
                    'roles': roles,
                    'id_proyecto': id_proyecto
                }
                return render(request, 'roles/ver_roles.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class VerTiposdeUSView(View):
    permisos = ["Ver TipoUserStory"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                tipos = TipoUserStory.objects.all().filter(proyecto=id_proyecto)
                context = {
                    'crear_tipoUS': True,
                    'tipos': tipos,
                    "id_proyecto": id_proyecto
                }
                return render(request, 'tipoUS/ver_tiposUS.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class CrearTiposUSView(View):
    form_class = FormTiposUS
    permisos = ["Crear TipoUserStory"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'tipoUS/creartipous.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            tipo_del_post = form.cleaned_data
            array_de_tipos = TipoUserStory.objects.all().filter(nombre=tipo_del_post['nombre'], proyecto_id=id_proyecto) | TipoUserStory.objects.\
                all().filter(nombre=tipo_del_post['prefijo'], proyecto_id=id_proyecto)

            if len(array_de_tipos) == 0:
                tipo = TipoUserStory.objects.create(nombre=tipo_del_post['nombre'], prefijo=tipo_del_post['prefijo']
                                                 , proyecto_id=id_proyecto)
                orden = OrdenEstado.objects.create(orden=1)
                EstadoUS.objects.create(nombre="TO DO", tipoUserStory=tipo, orden=orden)
                orden = OrdenEstado.objects.create(orden=2)
                EstadoUS.objects.create(nombre="DOING", tipoUserStory=tipo, orden=orden)
                orden = OrdenEstado.objects.create(orden=3)
                EstadoUS.objects.create(nombre="DONE", tipoUserStory=tipo, orden=orden)
                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'tipoUS/creartipous.html', {'form': form})
            return redirect('tiposUS', id_proyecto)
        return render(request, 'tipoUS/creartipous.html', {'form': form})


class DetalleTiposUSView(View):
    permisos = ["Ver TipoUserStory"]

    def get(self, request, id_proyecto, id_tipous):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                tipo = TipoUserStory.objects.get(id=id_tipous)
                estados = EstadoUS.objects.all().filter(tipoUserStory_id=id_tipous)
                context = {
                    'tipo': tipo,
                    'estados': estados,
                    'id_proyecto': id_proyecto,
                    'id_tipous': id_tipous
                }
                return render(request, 'tipoUS/detalle_tipoUS.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class CrearEstadosUSView(View):
    form_class = FormEstadoUS
    permisos = ["Crear EstadoUS"]

    def get(self, request, id_proyecto, id_tipous):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                return render(request, 'tipoUS/crearestadous.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_tipous):
        form = self.form_class(request.POST)
        if form.is_valid():
            estado_del_post = form.cleaned_data
            array_de_estados = EstadoUS.objects.all().filter(nombre=estado_del_post['nombre'],
                                                             tipoUserStory_id=id_tipous)

            if len(array_de_estados) == 0:
                tipo = TipoUserStory.objects.get(id=id_tipous)
                if not tipo.userstory_set.exists():
                    EstadoUS.objects.create(nombre=estado_del_post['nombre'], tipoUserStory=tipo,
                                            orden=OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=id_tipous)))
                    messages.success(request, 'Creado exitosamente!')
                else:
                    return redirect('detalle_tipoUS', id_proyecto, id_tipous)
            else:
                return render(request, 'tipoUS/crearestadous.html', {'form': form})
            return redirect('detalle_tipoUS', id_proyecto, id_tipous)
        return render(request, 'tipoUS/crearestadous.html', {'form': form})


class CrearUSView(View):
    form_class = FormUS
    permisos = ["Crear UserStory"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                form = self.form_class()
                form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
                return render(request, 'US/crearus.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto):
        form = self.form_class(request.POST)
        if form.is_valid():
            us = form.cleaned_data
            array_de_us = UserStory.objects.all().filter(nombre=us['nombre'], proyecto_id=id_proyecto)

            if len(array_de_us) == 0:
                p = Proyecto.objects.get(id=id_proyecto)
                estado_inicial = EstadoUS.objects.get(nombre="TO DO", tipoUserStory=us['tipo'])
                prioridad = round(0.6 * us["prioridad_de_negocio"] + 0.5 * us["prioridad_tecnica"])
                UserStory.objects.create(nombre=us['nombre'], descripcion=us['descripcion'], proyecto=p,
                                         tipo=us['tipo'], estado=estado_inicial, prioridad=prioridad,
                                         duracion=us['duracion'], prioridad_de_negocio=us['prioridad_de_negocio'],
                                         prioridad_tecnica=us['prioridad_tecnica'])

                messages.success(request, 'Creado exitosamente!')
            else:
                return render(request, 'US/crearus.html', {'form': form})
            return redirect('ver_US', id_proyecto)
        return render(request, 'US/crearus.html', {'form': form})


class VerUSView(View):
    permisos = ["Ver UserStory"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                uss = UserStory.objects.all().filter(proyecto=id_proyecto)
                context = {
                    'uss': uss,
                    'id_proyecto': id_proyecto
                }
                return render(request, 'US/ver_US.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class ActualizarUSView(View):
    form_class = FormUS
    permisos = ["Editar UserStory"]

    def get(self, request, id_proyecto, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                us = UserStory.objects.get(id=id_us)
                form = FormUS(instance=us)
                form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
                return render(request, 'US/editarus.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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
            return redirect('ver_US', id_proyecto)
        return render(request, 'US/editarus.html', {'form': form})


class BorrarUSView(View):
    form_class = FormUS
    permisos = ["Borrar UserStory"]

    def get(self, request, id_proyecto, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                us = UserStory.objects.get(id=id_us)
                form = FormUS(instance=us)
                return render(request, 'US/borrarus.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_us):
        us = UserStory.objects.get(id=id_us)

        us.delete()

        return redirect('ver_US', id_proyecto)


class DetalleEquipoView(View):
    permisos = ["Ver Equipo"]

    def get(self, request, id_proyecto, id_equipo):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
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
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class ActualizarEquipoView(View):
    permisos = ["Editar Equipo"]

    def get(self, request, id_proyecto, id_equipo):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                equipo = Equipo.objects.get(id=id_equipo)
                form = FormCrearEquipo(instance=equipo)
                return render(request, 'equipo/editarequipo.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_equipo):
        equipo = Equipo.objects.get(id=id_equipo)
        form = FormCrearEquipo(request.POST, instance=equipo)
        if form.is_valid():
            form.save()

            return redirect('ver_equipo', id_proyecto, id_equipo)
        return render(request, 'US/editarus.html', {'form': form})





class CrearSprint(View):
    form_class = FormSprint
    permisos = ["Crear Sprint"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                proyecto_en_proceso = self.verificar_estado_proyecto(id_proyecto=id_proyecto)
                no_hay_otro_sprint_en_planificacion = self.verificar_cantidad_de_sprints(id_proyecto=id_proyecto)
                if proyecto_en_proceso and no_hay_otro_sprint_en_planificacion:
                    form = self.form_class()
                    form.fields['product_backlog'].queryset = UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id__isnull=True)
                    return render(request, 'sprint/crearsprint.html', {'form': form})
                elif not proyecto_en_proceso:
                    return render(request, 'sprint/warning.html', {"mensajeerror": "El proyecto no esta iniciado!"})
                elif not no_hay_otro_sprint_en_planificacion:
                    return render(request, 'sprint/warning.html', {"mensajeerror": "Ya existe otro sprint en planificacion!"})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

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
            return redirect('detalle_proyecto', id_proyecto)
        return render(request, 'sprint/crearsprint.html', {'form': form})

    def verificar_estado_proyecto(self, id_proyecto):
        try:
            proyecto = Proyecto.objects.get(id=id_proyecto)
            if proyecto.estado == EstadoProyecto.EN_PROCESO:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def verificar_cantidad_de_sprints(self, id_proyecto):
        sprints = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoSprint.NO_INICIADO)
        if len(sprints) == 0:
            return True
        else:
            return False



class DetalleSprintView(View):
    permisos = ["Ver Sprint"]

    def get(self, request, id_proyecto, id_sprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos)
            if tiene_permisos:
                user_stories = UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id=id_sprint)
                sprint = Sprint.objects.get(id = id_sprint)
                context = {
                    'user_stories': user_stories,
                    'id_proyecto':id_proyecto,
                    "sprint" : sprint
                }
                return render(request, 'sprint/detalle_sprint.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class  verProductBacklog(View):
    permisos = ["Ver ProductBakclog"]

    def get(self, request, id_proyecto):
        usuario: Usuario = request.user
        if usuario.es_admin() or usuario.es_scrum_master(id_proyecto):
            uss = UserStory.objects.all().filter(proyecto=id_proyecto)
            context = {
                'uss': uss,
                'id_proyecto': id_proyecto
            }
        else:
            context = {
                "uss": [],
                'id_proyecto': id_proyecto
            }
        return render(request, 'backlog/ver_product_backlog.html', context)

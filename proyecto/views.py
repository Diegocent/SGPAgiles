
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.views import View
from .forms import FormCrearProyecto, FormCrearEquipo, FormIniciarProyecto, FormRolProyecto, FormTiposUS, FormEstadoUS, \
    FormUS, FormSprint, FormMiembroSprint, FormUSSprint, FormImportarMainPage, FormImportarRolesProyecto, \
    FormImportarTiposDeUS, FormAsignarDevAUserStory, FormAgregarTrabajoUS, FormAsignarRolAUsuario
from .models import Proyecto, EstadoProyecto, Equipo, TipoUserStory, UserStory, EstadoUS, Sprint, OrdenEstado, \
    EstadoSprint, MiembrosSprint, HistorialUS
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
            scrum = self.crearRoles(proyecto)

            usuario: Usuario = cleaned_data["scrum_master"]
            usuario.rolProyecto.add(scrum)
            usuario.save()

            equipo = Equipo.objects.create(nombre="")
            equipo.miembros.add(usuario)

            proyecto.equipo = equipo
            proyecto.save()

            messages.success(request, 'Creado exitosamente!')
            return redirect('ver_proyectos')
        return render(request, 'crear_proyecto.html', {'form': form})

    @staticmethod
    def crearRoles(proyecto):
        scrum = RolProyecto.objects.create(nombre="Scrum Master",
                                           descripcion="Scrum Master del Proyecto.",
                                           proyecto=proyecto)
        scrum.agregar_permisos([
            "Ver RolProyecto",
            "Crear RolProyecto",
            "Editar RolProyecto",
            "Borrar RolProyecto",
            "Ver Equipo",
            "Crear Equipo",
            "Editar Equipo",
            "Ver Proyecto",
            "Editar Proyecto",
            "Iniciar Proyecto",
            "Cancelar Proyecto",
            "Ver Sprint",
            "Crear Sprint",
            "Editar Sprint",
            "Iniciar Sprint",
            "Cancelar Sprint",
            "Ver TipoUserStory",
            "Crear TipoUserStory",
            "Editar TipoUserStory",
            "Borrar TipoUserStory",
            "Ver EstadoUS",
            "Crear EstadoUS",
            "Editar EstadoUS",
            "Borrar EstadoUS",
            "Ver UserStory",
            "Crear UserStory",
            "Editar UserStory",
            "Borrar UserStory",
            "Ver ProductBacklog",
            "Crear ProductBacklog",
            "Editar ProductBacklog",
            "Borrar ProductBacklog",
            "Ver Kanban",
        ])
        dev = RolProyecto.objects.create(nombre="Developer",
                                         descripcion="Developer del Proyecto.",
                                         proyecto=proyecto)
        dev.agregar_permisos([
            "Ver RolProyecto",
            "Ver Permiso",
            "Ver Usuario",
            "Ver Equipo",
            "Ver Proyecto",
            "Ver Sprint",
            "Ver TipoUserStory",
            "Ver EstadoUS",
            "Ver UserStory",
            "Ver ProductBacklog",
            "Ver Kanban",
            "Cambiar EstadoUS",
            "Editar Kanban",
            "Cargar trabajo UserStory",
        ])
        return scrum


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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
                if len(miembro.rolProyecto.all().filter(proyecto_id=id_proyecto))==0:
                    miembro.rolProyecto.add(RolProyecto.objects.get(nombre="Developer", proyecto_id=id_proyecto))
                    miembro.save()
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
                messages.error(request, "Ya existe un rol con ese nombre")

            return redirect('ver_roles', id_proyecto)
        return render(request, 'roles/crear_rol_proyecto.html', {'form': form})


class VerRolesProyectoView(View):
    permisos = ["Ver RolProyecto"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            array_de_tipos = TipoUserStory.objects.all().filter(nombre=tipo_del_post['nombre'], proyecto_id=id_proyecto) | TipoUserStory.objects. \
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
                numero = UserStory.obtener_ultimo_valor_de_us(id_proyecto=id_proyecto)
                user_story = UserStory.objects.create(numero=numero,
                                                      nombre=us['nombre'], descripcion=us['descripcion'], proyecto=p,
                                                      tipo=us['tipo'], estado=estado_inicial,
                                                      duracion=us['duracion'], prioridad_de_negocio=us['prioridad_de_negocio'],
                                                      prioridad_tecnica=us['prioridad_tecnica'])

                user_story.calcular_prioridad()
                HistorialUS.objects.create(log="User Story creado.", fecha=date.today(),
                                           user_story=user_story, usuario=request.user, horas_trabajadas=0)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                us = UserStory.objects.get(id=id_us)
                if us.sprint is None:
                    form = FormUS(instance=us)
                    form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
                    return render(request, 'US/editarus.html', {'form': form})
                elif us.sprint.estado == EstadoSprint.NO_INICIADO:
                    form = FormUS(instance=us)
                    form.fields['tipo'].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto)
                    return render(request, 'US/editarus.html', {'form': form})
                else:
                    messages.error(request, 'No se puede editar un US asignado a un sprint!')
                    return redirect("detalle_proyecto", id_proyecto=id_proyecto)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_us):
        us_obj = UserStory.objects.get(id=id_us)
        form = FormUS(request.POST, instance=us_obj)
        if form.is_valid():
            us_form = form.cleaned_data
            array_de_us = UserStory.objects.all().filter(nombre=us_form['nombre'],
                                                         proyecto_id=id_proyecto).exclude(id=id_us)

            if len(array_de_us) == 0:
                form.save()
                HistorialUS.objects.create(log="User Story fue editado.", fecha=date.today(),
                                           user_story_id=id_us, usuario=request.user, horas_trabajadas=0)
                messages.success(request, 'Creado exitosamente!')
                if us_obj.sprint is not None:
                    return redirect("ver_sprint", id_proyecto, us_obj.sprint.id)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                equipo = Equipo.objects.get(id=id_equipo)
                miembros = equipo.miembros.all()

                context = {
                    'equipo': equipo,
                    'miembros': miembros,
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
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

            self.eliminar_roles_de_miembros_eliminados(equipo_ant=equipo.miembros,
                                                       equipo_nuevo=form.cleaned_data["miembros"],
                                                       id_proyecto=id_proyecto)

            for miembro in form.cleaned_data["miembros"]:
                if len(miembro.rolProyecto.all().filter(proyecto_id=id_proyecto)) == 0:
                    miembro.rolProyecto.add(RolProyecto.objects.get(nombre="Developer", proyecto_id=id_proyecto))
                    miembro.save()
                equipo.miembros.add(miembro)


            form.save()

            return redirect('ver_equipo', id_proyecto, id_equipo)
        return render(request, 'US/editarus.html', {'form': form})

    def eliminar_roles_de_miembros_eliminados(self, equipo_ant, equipo_nuevo, id_proyecto):
        miembros_viejos = equipo_ant.all()
        miembros_nuevos = equipo_nuevo.all()
        miembros_eliminados = []
        for miembro_viejo in miembros_viejos:
            if miembro_viejo not in miembros_nuevos:
                miembro_viejo.rolProyecto.remove(*miembro_viejo.rolProyecto.filter(proyecto_id=id_proyecto))

        return miembros_eliminados


class CrearSprint(View):
    form_class = FormSprint
    permisos = ["Crear Sprint"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                proyecto_en_proceso = self.verificar_estado_proyecto(id_proyecto=id_proyecto)
                no_hay_otro_sprint_en_planificacion = self.verificar_cantidad_de_sprints(id_proyecto=id_proyecto)
                if proyecto_en_proceso and no_hay_otro_sprint_en_planificacion:
                    form = self.form_class()
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
            proyecto_en_proceso = self.verificar_estado_proyecto(id_proyecto=id_proyecto)
            no_hay_otro_sprint_en_planificacion = self.verificar_cantidad_de_sprints(id_proyecto=id_proyecto)
            if proyecto_en_proceso and no_hay_otro_sprint_en_planificacion:
                sprintform = form.cleaned_data

                p = Proyecto.objects.get(id=id_proyecto)
                numero = Sprint.obtener_ultimo_valor_de_sprint(id_proyecto=id_proyecto)
                sprint = Sprint.objects.create(numero=numero, descripcion=sprintform['descripcion'],
                                               proyecto=p, estado=EstadoSprint.NO_INICIADO, duracion=sprintform["duracion"])
                return redirect('ver_sprint', id_proyecto, sprint.id)
            elif not proyecto_en_proceso:
                return render(request, 'sprint/warning.html', {"mensajeerror": "El proyecto no esta iniciado!"})
            elif not no_hay_otro_sprint_en_planificacion:
                return render(request, 'sprint/warning.html',
                              {"mensajeerror": "Ya existe otro sprint en planificacion!"})
        else:
            return render(request, 'sprint/crearsprint.html', {'form': form})
        return redirect('detalle_proyecto', id_proyecto)

    @staticmethod
    def verificar_estado_proyecto(id_proyecto):
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
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                user_stories = UserStory.objects.filter(proyecto_id=id_proyecto, sprint_id=id_sprint)
                sprint = Sprint.objects.get(id = id_sprint)
                devs = MiembrosSprint.objects.filter(sprint_id=id_sprint)
                hay_otro_sprint_en_proceso = Sprint.hay_otros_sprints_en_proceso(id_proyecto=id_proyecto)
                context = {
                    'devs': devs,
                    'user_stories': user_stories,
                    'id_proyecto':id_proyecto,
                    "sprint" : sprint,
                    "hay_otro_sprint_en_proceso" : hay_otro_sprint_en_proceso
                }
                return render(request, 'sprint/detalle_sprint.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class ActualizarSprintView(View):
    form_class = FormSprint
    permisos = ["Editar Sprint"]

    def get(self, request, id_proyecto, id_sprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
                if sprint.estado == EstadoSprint.NO_INICIADO:
                    form = self.form_class(instance=sprint)
                    return render(request, 'sprint/editarsprint.html', {'form': form})
                else:
                    messages.error(request, 'No se puede editar un US asignado a un sprint!')
                    return redirect("detalle_proyecto", id_proyecto=id_proyecto)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint):
        sprint_obj = Sprint.objects.get(id=id_sprint)
        form = self.form_class(request.POST, instance=sprint_obj)
        if form.is_valid():

            form.save()
            sprint = sprint_obj
            miembros = MiembrosSprint.objects.filter(sprint_id=sprint.id)
            for miembro in miembros:
                miembro.capacidad = sprint.duracion * miembro.carga_horaria
                miembro.save()

            messages.success(request, 'Sprint fue editado exitosamente!')

            return redirect('ver_sprint', id_proyecto, id_sprint)
        return render(request, 'sprint/editarsprint.html', {'form': form})


class verProductBacklog(View):
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


class AsignarMiembroASprint(View):
    permisos = ["Editar Sprint"]

    form_class = FormMiembroSprint

    def get(self, request, id_proyecto, id_sprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:

                try:
                    sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al Sprint con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)

                form = self.form_class()
                form.fields["miembro"] = forms. \
                    ModelChoiceField(label="Miembro a ingresar al Sprint.",
                                     help_text="Seleccione al developer que entrara al sprint.",
                                     queryset=Usuario.objects.filter(
                                         rolProyecto__proyecto_id=id_proyecto,
                                         rolProyecto__nombre="Developer").exclude(miembrossprint__sprint_id=id_sprint)
                                     )
                return render(request, 'sprint/asignarmiembrosprint.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint):
        form = self.form_class(request.POST)
        if form.is_valid():

            form = form.cleaned_data
            try:
                sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
            except ObjectDoesNotExist:
                messages.error(request, message="No se encuentra al Sprint para este proyecto")
                return redirect("detalle_proyecto", id_proyecto)

            capacidad = form["carga_horaria"] * sprint.duracion

            MiembrosSprint.objects.create(sprint=sprint, carga_horaria=form["carga_horaria"],
                                          miembro=form["miembro"],
                                          capacidad=capacidad)
            sprint.save()

            messages.success(request, message="Miembro agregado exitosamente.")
            return redirect("ver_sprint", id_proyecto, id_sprint)
        else:
            return render(request, 'sprint/asignarmiembrosprint.html', {'form': form})


class AsignarUSASprint(View):
    permisos = ["Editar Sprint"]

    form_class = FormUSSprint

    def get(self, request, id_proyecto, id_sprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:

                try:
                    sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al Sprint con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)

                if sprint.estado==EstadoSprint.EN_PROCESO:
                    messages.error(request, message="No se puede agregar un US a un Sprint ya iniciado")
                    return redirect("detalle_proyecto", id_proyecto)

                form = self.form_class()
                form.fields["user_stories"].queryset = UserStory.objects.filter(
                    proyecto_id=id_proyecto,
                    sprint__isnull=True
                ).order_by('-prioridad')

                return render(request, 'sprint/asignarussprint.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.cleaned_data
            try:
                sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
            except ObjectDoesNotExist:
                messages.error(request, message="No se encuentra al Sprint para este proyecto")
                return redirect("detalle_proyecto", id_proyecto)

            if sprint.estado == EstadoSprint.EN_PROCESO:
                messages.error(request, message="No se puede agregar un US a un Sprint ya iniciado")
                return redirect("detalle_proyecto", id_proyecto)

            for us in form["user_stories"]:
                us: UserStory
                us.sprint = sprint
                HistorialUS.objects.create(log="User Story asignado al Sprint {}".format(sprint.numero),
                                           fecha=date.today(),
                                           user_story_id=us.id, usuario=request.user, horas_trabajadas=0)
                us.save()

            messages.success(request, message="Miembro agregado exitosamente.")
            return redirect("ver_sprint", id_proyecto, id_sprint)
        else:
            return render(request, 'sprint/asignarussprint.html', {'form': form})


class BorrarUSASprint(View):
    permisos = ["Editar Sprint"]

    def get(self, request, id_proyecto, id_sprint, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:

                try:
                    sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
                    us = UserStory.objects.get(sprint_id=id_sprint, proyecto_id=id_proyecto, id=id_us)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al Sprint con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)

                if sprint.estado == EstadoSprint.EN_PROCESO:
                    messages.error(request, message="No se puede borrar un US de un Sprint ya iniciado")
                    return redirect("detalle_proyecto", id_proyecto)

                return render(request, 'sprint/borrarussprint.html',)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint, id_us):

        try:
            sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
        except ObjectDoesNotExist:
            messages.error(request, message="No se encuentra al Sprint para este proyecto")
            return redirect("detalle_proyecto", id_proyecto)

        if sprint.estado == EstadoSprint.EN_PROCESO:
            messages.error(request, message="No se puede borrar un US de un Sprint ya iniciado")
            return redirect("ver_sprint", id_proyecto, id_sprint)

        try:
            us = UserStory.objects.get(sprint_id=id_sprint, proyecto_id=id_proyecto, id=id_us)
        except ObjectDoesNotExist:
            messages.error(request, message="No se encuentra al Sprint para este proyecto")
            return redirect("detalle_proyecto", id_proyecto)

        us.sprint = None
        HistorialUS.objects.create(log="User Story removido del Sprint {}".format(sprint.numero),
                                   fecha=date.today(),
                                   user_story_id=us.id, usuario=request.user, horas_trabajadas=0)
        us.save()

        messages.success(request, message="Miembro eliminado exitosamente.")
        return redirect("ver_sprint", id_proyecto, id_sprint)


class ActualizarMiembrosSprintView(View):
    permisos = ["Editar Sprint"]

    def get(self, request, id_proyecto, id_sprint, id_miembrosprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    miembrosprint = MiembrosSprint.objects.get(id=id_miembrosprint, sprint_id=id_sprint)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra el objeto requerido. Verifique parametros")
                    return redirect("detalle_proyecto", id_proyecto)
                form = FormMiembroSprint(instance=miembrosprint)
                return render(request, 'sprint/editarmiembrosprint.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint, id_miembrosprint):
        miembrosprint = MiembrosSprint.objects.get(id=id_miembrosprint, sprint_id=id_sprint)
        form = FormMiembroSprint(request.POST, instance=miembrosprint)

        sprint = Sprint.objects.get(id=id_sprint)

        if form.is_valid():


            form = form.cleaned_data
            miembrosprint.miembro = form["miembro"]
            miembrosprint.carga_horaria = form["carga_horaria"]
            miembrosprint.capacidad = form["carga_horaria"] * sprint.duracion
            miembrosprint.save()

            sprint.save()

            messages.success(request, "Miembro del sprint editado correctamente")
            return redirect('ver_sprint', id_proyecto, id_sprint)
        return render(request, 'sprint/editarmiembrosprint.html', {'form': form})


class BorrarMiembrosSprintView(View):
    permisos = ["Editar Sprint"]

    def get(self, request, id_proyecto, id_sprint, id_miembrosprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    miembrosprint = MiembrosSprint.objects.get(id=id_miembrosprint, sprint_id=id_sprint)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra el objeto requerido. Verifique parametros")
                    return redirect("detalle_proyecto", id_proyecto)
                form = FormMiembroSprint(instance=miembrosprint)
                return render(request, 'sprint/eliminarmiembrosprint.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint, id_miembrosprint):
        miembrosprint = MiembrosSprint.objects.get(id=id_miembrosprint, sprint_id=id_sprint)

        sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)

        sprint.save()

        miembrosprint.delete()

        messages.success(request, "Miembro del sprint eliminado correctamente")
        return redirect('ver_sprint', id_proyecto, id_sprint)


class VerSprintsView(View):

    permisos = ["Ver Sprint"]

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                hay_otro_sprint_planificado = Sprint.hay_otros_sprints_en_planificacion(id_proyecto=id_proyecto)
                hay_otro_sprint_iniciado = Sprint.hay_otros_sprints_en_proceso(id_proyecto=id_proyecto)
                sprint_planeados = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoSprint.NO_INICIADO)
                sprint_iniciados = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoSprint.EN_PROCESO)
                sprint_finalizados = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoSprint.TERMINADO)
                sprint_cancelados = Sprint.objects.filter(proyecto_id=id_proyecto, estado=EstadoSprint.CANCELADO)
                context = {
                    'sprint_planeados': sprint_planeados,
                    'sprint_iniciados': sprint_iniciados,
                    'sprint_finalizados': sprint_finalizados,
                    'sprint_cancelados': sprint_cancelados,
                    'id_proyecto': id_proyecto,
                    "hay_otro_sprint_iniciado" : hay_otro_sprint_iniciado,
                    "hay_otro_sprint_planificado" : hay_otro_sprint_planificado
                }
                return render(request, 'sprint/versprints.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class ImportarMainPageView(View):
    permisos = ["Editar RolProyecto", "Editar TipoUserStory"]

    form_class = FormImportarMainPage

    def get(self, request, id_proyecto):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                form = self.form_class({'id_proyecto':id_proyecto})
                form.fields["proyecto"].queryset = Proyecto.objects.all().exclude(id=id_proyecto)
                return render(request, 'proyecto/importarMainPage.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto):

        form = FormImportarMainPage(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            accion = form["acciones"]
            proyecto = form["proyecto"]
            if accion == '1':
                return redirect("importar_roles", id_proyecto, proyecto.id)
            elif accion == '2':
                return redirect("importar_tipos", id_proyecto, proyecto.id)
        return render(request, 'proyecto/importarMainPage.html', {'form': form})


class ImportarRolesDeOtroProyectoView(View):

    permisos = ["Editar RolProyecto", "Editar TipoUserStory"]

    form_class = FormImportarRolesProyecto

    def get(self, request, id_proyecto, id_proyecto_a_importar):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                form = self.form_class()
                form.fields["roles"].queryset = RolProyecto.objects.filter(proyecto_id=id_proyecto_a_importar)
                return render(request, 'proyecto/importarRoles.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_proyecto_a_importar):

        form = FormImportarRolesProyecto(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            roles = form["roles"]

            for rol in roles:
                rol: RolProyecto
                rol.pk = None
                rol._state.adding = True
                rol.nombre += " - copy"
                rol.proyecto_id = id_proyecto
                roles_array = RolProyecto.objects.filter(proyecto_id=id_proyecto, nombre=rol.nombre)
                if len(roles_array) == 0:
                    rol.save()
            return redirect("ver_roles", id_proyecto)
        return render(request, 'proyecto/importarRoles.html', {'form': form})


class ImportarTiposUSDeOtroProyectoView(View):

    permisos = ["Editar RolProyecto", "Editar TipoUserStory"]

    form_class = FormImportarTiposDeUS

    def get(self, request, id_proyecto, id_proyecto_a_importar):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                form = self.form_class()
                form.fields["tipos"].queryset = TipoUserStory.objects.filter(proyecto_id=id_proyecto_a_importar)
                return render(request, 'proyecto/importarTipos.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def copiar_estados(self, id_tipo_anterior, tipo_nuevo):
        estados_del_tipo_anterior = EstadoUS.objects.filter(tipoUserStory_id=id_tipo_anterior)
        for estado in estados_del_tipo_anterior:
            estado.pk = None
            estado._state.adding = True
            estado.tipoUserStory = tipo_nuevo

            orden = estado.orden
            orden.pk = None
            orden._state.adding = True
            orden.save()
            estado.orden = orden

            estado.save()

    def post(self, request, id_proyecto, id_proyecto_a_importar):

        form = self.form_class(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            tipos = form["tipos"]

            for tipo in tipos:
                tipo: TipoUserStory
                id_tipo_anterior = tipo.id
                tipo.pk = None
                tipo._state.adding = True
                tipo.nombre += " - copy"
                tipo.proyecto_id = id_proyecto
                tipos_array = TipoUserStory.objects.filter(proyecto_id=id_proyecto, nombre=tipo.nombre)
                if len(tipos_array) == 0:
                    tipo.save()
                self.copiar_estados(id_tipo_anterior=id_tipo_anterior, tipo_nuevo=tipo)
            return redirect("tiposUS", id_proyecto)
        return render(request, 'proyecto/importarRoles.html', {'form': form})


class IniciarSprint(View):

    permisos = ["Iniciar Sprint"]

    def get(self, request, id_proyecto, id_sprint):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    sprint = Sprint.objects.get(id=id_sprint, proyecto_id=id_proyecto)
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al Sprint con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)

                tiene_miembros = sprint.tiene_miembros
                tiene_user_stories = sprint.tiene_user_stories
                hay_otros_sprints_en_proceso = sprint.hay_otros_sprints_en_proceso(id_proyecto=id_proyecto)

                if tiene_miembros and tiene_user_stories and not hay_otros_sprints_en_proceso:
                    return render(request, 'sprint/iniciarsprint.html')
                elif not tiene_miembros:
                    messages.error(request, message="No se puede iniciar un sprint sin miembros!")
                elif not tiene_user_stories:
                    messages.error(request, message="No se puede iniciar un sprint sin User Stories!")
                elif not hay_otros_sprints_en_proceso:
                    messages.error(request, message="No se puede iniciar un sprint teniendo otro sprint en proceso!")
                return redirect("ver_sprints", id_proyecto)

            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_sprint):
        sprint = Sprint.objects.get(proyecto_id=id_proyecto, id=id_sprint)
        sprint.fecha_inicio = date.today()
        sprint.estado = EstadoSprint.EN_PROCESO
        sprint.save()
        self.guardar_eventos_en_historial(sprint=sprint, request=request)
        messages.success(request, 'Creado exitosamente!')
        return redirect('detalle_proyecto', id_proyecto)

    @staticmethod
    def guardar_eventos_en_historial(sprint, request):
        user_stories = UserStory.objects.filter(sprint=sprint)
        for us in user_stories:
            HistorialUS.objects.create(log="Sprint {} iniciado.".format(sprint.numero),
                                       fecha=date.today(),
                                       user_story_id=us.id, usuario=request.user, horas_trabajadas=0)


class DetalleUSView(View):
    permisos = ["Ver UserStory"]

    def get(self, request, id_proyecto, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    us = UserStory.objects.get(proyecto_id=id_proyecto, id=id_us)
                except ObjectDoesNotExist:
                    messages.error(request, "User Story no existe en este proyecto.")
                    return redirect("detalle_proyecto", id_proyecto)

                historiales = HistorialUS.objects.filter(user_story_id=id_us)
                horas_trabajadas = us.total_horas_trabajadas
                puede_asignar_dev = user.tiene_permisos(permisos=["Editar UserStory"], id_proyecto=id_proyecto)
                context = {
                    'historiales': historiales,
                    'horas_trabajadas': horas_trabajadas,
                    'us' : us,
                    'id_proyecto': id_proyecto,
                    'puede_asignar_dev' : puede_asignar_dev
                }
                return render(request, 'US/detalle_us.html', context)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")


class AgregarTrabajoAUserStory(View):
    form_class = FormAgregarTrabajoUS
    permisos = ["Cargar trabajo UserStory"]

    def get(self, request, id_proyecto, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    us = UserStory.objects.get(id=id_us, proyecto_id=id_proyecto)
                    sprint = us.sprint
                    if sprint is None:
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al User Story con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)
                if sprint.estado == EstadoSprint.EN_PROCESO:
                    usuario_es_su_desarrollador = False
                    if us.desarrollador == user:
                        usuario_es_su_desarrollador = True

                    if usuario_es_su_desarrollador or user.es_admin():
                        form = self.form_class()
                        return render(request, 'HUS/cargartrabajo.html', {"form": form})
                    elif not usuario_es_su_desarrollador:
                        messages.error(request, message="No podes cargarle trabajo a un US sin ser su desarrolador!")
                    return redirect("detalle_proyecto", id_proyecto)
                else:
                    messages.error(request, message="No podes cargarle trabajo a un US sin que el sprint este en proceso!")
                    return redirect("detalle_proyecto", id_proyecto)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_us):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():

            cleaned_data = form.cleaned_data


            HistorialUS.objects.create(log=cleaned_data["log"], user_story_id=id_us,
                                       horas_trabajadas=cleaned_data["horas_trabajadas"],
                                       fecha=date.today(), usuario_id=request.user.id, archivos=cleaned_data["archivos"]
                                       )

            messages.success(request, 'Creado exitosamente!')
            return redirect('detalle_US', id_proyecto, id_us)
        else:
            return redirect("detalle_proyecto", id_proyecto)


class AsignarDevAUserStory(View):

    form_class = FormAsignarDevAUserStory
    permisos = ["Editar UserStory"]

    def get(self, request, id_proyecto, id_us):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    us = UserStory.objects.get(id=id_us, proyecto_id=id_proyecto)
                    if us.sprint is None:
                        raise ObjectDoesNotExist
                    sprint = us.sprint
                except ObjectDoesNotExist:
                    messages.error(request, message="No se encuentra al User Story con esos parametros.")
                    return redirect("detalle_proyecto", id_proyecto)
                if sprint.estado == EstadoSprint.EN_PROCESO:
                    form = self.form_class()
                    form.fields["desarrollador"].queryset = Usuario.objects.filter(miembrossprint__sprint_id=us.sprint)

                    return render(request, 'US/asignar_dev.html', {"form":form})
                else:
                    messages.error(request, message="El sprint no esta iniciado!")
                    return redirect("detalle_proyecto", id_proyecto)
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_us):
        form = self.form_class(request.POST)

        if form.is_valid():

            form = form.cleaned_data
            try:
                us = UserStory.objects.get( proyecto_id=id_proyecto, id=id_us)
            except ObjectDoesNotExist:
                messages.error(request, message="No se encuentra al Sprint para este proyecto")
                return redirect("detalle_proyecto", id_proyecto)

            dev: Usuario = form["desarrollador"]
            us.desarrollador = dev
            us.save()

            HistorialUS.objects.create(log="{} se encargara de desarrollar este US.".format(dev.email),
                                       fecha=date.today(),
                                       user_story_id=us.id, usuario=request.user, horas_trabajadas=0)

            messages.success(request, message="Miembro agregado exitosamente.")
            return redirect("detalle_US", id_proyecto, id_us)
        else:
            return render(request, 'sprint/asignarussprint.html', {'form': form})


class ActualizarRolProyecto(View):
    form_class = FormRolProyecto
    permisos = ["Editar RolProyecto"]

    def get(self, request, id_proyecto, id_rol):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    rol = RolProyecto.objects.get(id=id_rol, proyecto_id=id_proyecto)
                except ObjectDoesNotExist:
                    messages.error(request, "No se encuentra el Rol de proyecto con esas caracteristicas")
                    return redirect("detalle_proyecto", id_proyecto)
                form = self.form_class(instance=rol)
                return render(request, 'roles/editar_rol_proyecto.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_rol):
        rol_obj = RolProyecto.objects.get(id=id_rol)
        form = self.form_class(request.POST, instance=rol_obj)
        if form.is_valid():
            rol_del_post = form.cleaned_data
            array_de_roles = RolProyecto.objects.all().filter(nombre=rol_del_post['nombre'], proyecto_id=id_proyecto).exclude(id=id_rol)
            if len(array_de_roles) == 0:
                form.save()
                rol_obj.permisos.clear()
                for permisos in rol_del_post['permisos']:
                    rol_obj.permisos.add(permisos)
                rol_obj.save()
                messages.success(request, 'Editado exitosamente!')
            else:
                messages.error(request, "Ya existe un rol con ese nombre")

            return redirect('ver_roles', id_proyecto)
        return render(request, 'roles/editar_rol_proyecto.html', {'form': form})


class AsignarRolProyectoAUsuario(View):
    form_class = FormAsignarRolAUsuario
    permisos = ["Editar RolProyecto"]

    def get(self, request, id_proyecto, id_equipo, id_usuario):
        user: Usuario = request.user
        if user.is_authenticated:
            tiene_permisos = user.tiene_permisos(permisos=self.permisos, id_proyecto=id_proyecto)
            if tiene_permisos:
                try:
                    usuario_a_asignar = Usuario.objects.get(id=id_usuario, equipo__id=id_equipo, equipo__proyecto__id=id_proyecto)
                except ObjectDoesNotExist:
                    messages.error(request, "No se encuentra el Rol de proyecto con esas caracteristicas")
                    return redirect("detalle_proyecto", id_proyecto)
                roles = usuario_a_asignar.rolProyecto.all().filter(proyecto_id=id_proyecto)
                form = self.form_class()
                form.fields["roles"].queryset = RolProyecto.objects.filter(proyecto_id=id_proyecto)
                if len(roles) > 0:
                    form.fields["roles"].initial = roles
                return render(request, 'roles/asignar_rol_proyecto.html', {'form': form})
            elif not tiene_permisos:
                return render(request, 'herramientas/forbidden.html', {'permisos': self.permisos})
        elif not user.is_authenticated:
            return redirect("home")

    def post(self, request, id_proyecto, id_equipo, id_usuario):
        form = self.form_class(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            roles = form["roles"]

            usuario_a_asignar = Usuario.objects.get(id=id_usuario, equipo__id=id_equipo, equipo__proyecto__id=id_proyecto)
            usuario_a_asignar.rolProyecto.clear()

            for rol in roles:
                usuario_a_asignar.rolProyecto.add(rol)
                usuario_a_asignar.save()
            messages.success(request, 'Rol de usuario editado exitosamente!')


            return redirect('ver_equipo', id_proyecto, id_equipo)
        return render(request, 'roles/asignar_rol_proyecto.html', {'form': form})
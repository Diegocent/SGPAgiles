from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from .forms import FormCrearProyecto, FormCrearEquipo, FormIniciarProyecto
from .models import Proyecto, EstadoProyecto, Equipo
from Usuario.models import Usuario, RolProyecto
from django.contrib import messages
from datetime import date
# Create your views here.
"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views en Proyecto:

1. **CrearProyectoView** - Se crea la vista del Proyecto (salta a la seccion [[views.py#CrearProyectoView]] )
2. **CrearEquipoView** - Se crea la vista para Equipo (salta a la seccion [[views.py#CrearEquipoView]] )
"""

class VerProyectosView(View, LoginRequiredMixin):
    def get(self, request):
        usuario: Usuario = request.user
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
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('ver_proyectos')
        return render(request, 'crear_proyecto.html', {'form': form})


class VerProyectosView(View, LoginRequiredMixin):

    def get(self, request):
        usuario: Usuario = request.user
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


class VerProyectoView(View, LoginRequiredMixin):

        def get(self, request, id_proyecto):
            usuario: Usuario = request.user
            p = Proyecto.objects.get(id=id_proyecto)
            equipo = p.equipo

            if equipo:
                miembros = equipo.miembros.all()

                if usuario not in miembros and not usuario.es_admin():
                    messages.warning(request, "No puedes ver este proyecto.")
                    return HttpResponseRedirect('ver_proyectos')
                context = {
                    "proyecto": p,
                    "equipo": equipo,
                    "miembros": miembros
                }
            else:
                if not usuario.es_admin():
                    messages.warning(request, "No puedes ver este proyecto.")
                    return HttpResponseRedirect('ver_proyectos')
                context = {
                    "proyecto": p
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


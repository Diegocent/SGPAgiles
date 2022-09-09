from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from .forms import FormCrearProyecto, FormCrearEquipo
from .models import Proyecto, EstadoProyecto, Equipo
from django.contrib import messages
# Create your views here.
"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views en Proyecto:

1. **CrearProyectoView** - Se crea la vista del Proyecto (salta a la seccion [[views.py#CrearProyectoView]] )
2. **CrearEquipoView** - Se crea la vista para Equipo (salta a la seccion [[views.py#CrearEquipoView]] )
"""
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
            Proyecto.objects.create(
                nombre=cleaned_data["nombre"],
                descripcion=cleaned_data["descripcion"],
                equipo=cleaned_data["equipo"],
                estado=EstadoProyecto.NO_INICIADO
            )
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('index.html')
        return render(request, 'crear_proyecto.html', {'form': form})

class CrearEquipoView(View, LoginRequiredMixin):
    form_class = FormCrearEquipo

    def get(self, request):
        if not request.user.es_admin():
            return HttpResponseRedirect('/')
        form = self.form_class()
        return render(request, 'crear_equipo.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Equipo.objects.create(
                nombre=cleaned_data["nombre"],
                miembros=cleaned_data["miembros"],
            )
            messages.success(request, 'Creado exitosamente!')
            return HttpResponseRedirect('index.html')
        return render(request, 'crear_proyecto.html', {'form': form})

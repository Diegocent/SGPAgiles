from .models import Equipo
from .models import Usuario
from django import forms



class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del proyecto', empty_value="Escriba el nombre del proyecto.")
    descripcion = forms.CharField(label='Descripcion del proyecto', empty_value="Describa el proyecto.")
    scrum_master = forms.ModelChoiceField(
        queryset=Usuario.objects.all(), label="Scrum Master",
        help_text="Seleccione el Scrum Master del proyecto."
    )


class FormCrearEquipo(forms.Form):
    nombre = forms.CharField(label='Nombre del equipo', empty_value="Escriba el nombre del equipo")
    miembros = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(), label="Miembros",
        help_text="Seleccione aqui a los miembros del equipo a crear.",
        widget = forms.CheckboxSelectMultiple()
    )


class FormIniciarProyecto(forms.Form):
    fecha_fin_estimada = forms.DateTimeField(required=True,
                                             label="Fecha estimada de fin",)

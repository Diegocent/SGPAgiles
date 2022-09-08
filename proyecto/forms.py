from .models import Equipo
from .models import Usuario
from django import forms


class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del proyecto', empty_value="Escriba el nombre del proyecto.")
    descripcion = forms.CharField(label='Descripcion del proyecto', empty_value="Describa el proyecto.")
    equipo = forms.ModelChoiceField(
        queryset=Equipo.objects.all(), label="Equipo", empty_label="Seleccione el equipo.",
        help_text="Seleccione aqui el equipo que llevara el proyecto."
    )

class FormCrearEquipo(forms.Form):
    nombre = forms.CharField(label='Nombre del equipo', empty_value="Escriba el nombre del equipo")
    miembros = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(), label="Miembros", empty_label="Seleccione a los miembros del equipo.",
        help_text="Seleccione aqui a los miembros del equipo a crear."
    )
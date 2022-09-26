from .models import Equipo, TipoUserStory
from Usuario.models import Permisos, Usuario
from django import forms



class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del Proyecto', empty_value="Escriba el nombre del proyecto.")
    descripcion = forms.CharField(label='Descripción del Proyecto', empty_value="Describa el proyecto.")
    scrum_master = forms.ModelChoiceField(
        queryset=Usuario.objects.all(), label="Scrum Master",
        help_text="Seleccione el Scrum Master del proyecto."
    )


class FormCrearEquipo(forms.Form):
    nombre = forms.CharField(label='Nombre del equipo', empty_value="Escriba el nombre del equipo")
    miembros = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(), label="Miembros",
        help_text="Seleccione aqui a los miembros del equipo a crear.",
        widget=forms.CheckboxSelectMultiple()
    )


class FormIniciarProyecto(forms.Form):
    fecha_fin_estimada = forms.DateTimeField(required=True,
                                             label="Fecha estimada de fin",)


class FormRolProyecto(forms.Form):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=100)
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permisos.objects.all(), widget=forms.CheckboxSelectMultiple())


class FormTiposUS(forms.Form):
    nombre = forms.CharField(max_length=100)
    prefijo = forms.CharField(max_length=5)


class FormEstadoUS(forms.Form):
    nombre = forms.CharField(max_length=100)


class FormUS(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    descripcion = forms.CharField(max_length=100)
    tipo = forms.ModelChoiceField(
        queryset=TipoUserStory.objects.all(), widget=forms.Select, required=True)
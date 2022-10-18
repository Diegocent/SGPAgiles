from django.forms import ModelForm

from .models import Equipo, TipoUserStory, UserStory, Sprint
from Usuario.models import Permisos, Usuario
from django import forms



class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del Proyecto', empty_value="Escriba el nombre del proyecto.")
    descripcion = forms.CharField(label='Descripción del Proyecto', empty_value="Describa el proyecto.")
    scrum_master = forms.ModelChoiceField(
        queryset=Usuario.objects.all(), label="Scrum Master",
        help_text="Seleccione el Scrum Master del proyecto."
    )


class FormCrearEquipo(ModelForm):
    class Meta:
        model = Equipo
        fields = ("nombre", "miembros")


class FormIniciarProyecto(forms.Form):
    fecha_fin_estimada = forms.DateTimeField(required=True,
                                             label="Fecha estimada de fin",)


class FormRolProyecto(forms.Form):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=100)
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permisos.objects.all(), label="Permisos",
        help_text="Seleccione los Permisos.")


class FormTiposUS(forms.Form):
    nombre = forms.CharField(max_length=100)
    prefijo = forms.CharField(max_length=5)


class FormEstadoUS(forms.Form):
    nombre = forms.CharField(max_length=100)


class FormUS(ModelForm):
    class Meta:
        model = UserStory
        fields = ["nombre", "descripcion", "tipo", "prioridad_de_negocio", "prioridad_tecnica", "duracion"]


class FormSprint(ModelForm):
    product_backlog = forms.ModelMultipleChoiceField(queryset=UserStory.objects.all())

    class Meta:
        model = Sprint
        fields = ["numero", "descripcion", "fecha_fin", ]

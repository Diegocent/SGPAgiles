
from django import forms


class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del proyecto')
    descripcion = forms.CharField(label='Descripcion del pdroyecto')
from django import forms

from Usuario.models import Permisos, Usuario, RolSistema


class FormRolSistema(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True)
    descripcion = forms.CharField(max_length=100)
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permisos.objects.all(), required=True)

    class Meta:
        model = RolSistema #Campos para nombre, descripcion, tipo, prioridad de negocio, prioridad de tecnica y la duracion que tendra
        fields = ["nombre", "descripcion", "permisos"]


class FormCrearPermisos(forms.Form):
    nombre = forms.CharField(label='Nombre del permiso', empty_value="Escriba el nombre del permiso.", required=True)
    descripcion = forms.CharField(label='Descripcion del permiso', empty_value="Describa el permiso.")



class FormAsignarRol(forms.Form):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=True, label="Usuario")
    rol = forms.ModelMultipleChoiceField(queryset=RolSistema.objects.all(), required=True, label="Rol")


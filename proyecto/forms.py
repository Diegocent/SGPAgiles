from django.forms import ModelForm

from .models import Equipo, TipoUserStory, UserStory, Sprint, MiembrosSprint, Proyecto, HistorialUS, AprobacionDeUS, \
    Feriado
from Usuario.models import Permisos, Usuario, RolProyecto
from django import forms

"""

Todos los forms para SGPAgiles 
Actualmente contamos con los siguientes views en Proyecto: 

1. **FormCrearProyecto** - Formulario para Crear Proyectos (salta a la seccion [[forms.py#FormCrearProyecto]])
2. **FormCrearEquipo** - Formulario para Crear Equipos (salta a la seccion [[forms.py#FormCrearEquipo]])
3. **FormIniciarProyecto** - Formulario para Iniciar Proyecto (salta a la seccion [[forms.py#FormIniciarProyecto]])
4. **FormRolProyecto** - Formulario para Crear Rol del Proyecto (salta a la seccion [[forms.py#FormRolProyecto]])
5. **FormTipoUs** - Formulario para Crear Tipo de User Story del Proyecto (salta a la seccion [[forms.py#FormTipoUS]])
6. **FormEstadoUS** - Formulario para Crear Estado de US (salta a la seccion [[forms.py#FormEstadoUS]])
7. **FormUS** - Formulario para Crear User Story (salta a la seccion [[forms.py#FormUS]])
8. **FormSprint** - Formulario para Crear Sprint (salta a la seccion [[forms.py#FormSprint]])
9. **FormMiembroSprint** - Formulario para Asignar Carga horaria al Sprint (salta a la seccion [[forms.py#FormMiembroSprint]])
10. **FormUSSprint** - Formulario para Asignar User Story al Sprint (salta a la seccion [[forms.py#FormUSSprint]])
11. **FormImportarMainPage** - Formulario para Importar las acciones a realizar y los proyectos (salta a la seccion [[forms.py#FormImportarMainPage]])
12. **FormImportarRolesProyecto** - Formulario para Importar los roles del proyectos (salta a la seccion [[forms.py#FormImportarRolesProyecto]])
13. **FormImportarTiposDeUS** - Formulario para Importar los tipos de User Story (salta a la seccion [[forms.py#FormImportarTiposDeUS]])
14. **FormAsignarDevAUserStory** - Formulario para asignar un desarrollador al User Story (salta a la seccion [[forms.py#FormAsignarDevAUserStory]])
15. **FormAgregarTrabajoUS** - Formulario para agregar trabajo a los User Story (salta a la seccion [[forms.py#FormAgregarTrabajoUS]])
16. **FromAgregarRolAUsuario** - Formulario para asignar roles al usuario (salta a la seccion [[forms.py#FormAgregarRolAUsuario]])
"""

class FormCrearProyecto(forms.Form):
    nombre = forms.CharField(label='Nombre del Proyecto', empty_value="Escriba el nombre del proyecto.", max_length=100) #Se ingresa el nombre del proyecto
    descripcion = forms.CharField(label='Descripción del Proyecto', empty_value="Describa el proyecto.", max_length=100) #Descripcion del proyecto
    scrum_master = forms.ModelChoiceField( #Scrum master que sera asignado
        queryset=Usuario.objects.all(), label="Scrum Master",
        help_text="Seleccione el Scrum Master del proyecto."
    )


class FormCrearEquipo(ModelForm):
    class Meta:
        model = Equipo
        fields = ("nombre", "miembros") #Nombre del equipo y los miembros que formaran parte de el


class FormIniciarProyecto(forms.Form):
    fecha_fin_estimada = forms.DateTimeField(required=True, #Se Asigna fecha estimativa del fin del proyecto
                                             label="Fecha estimada de fin",)


class FormRolProyecto(ModelForm):
    nombre = forms.CharField(max_length=100, label="Nombre") #Nombre del rol
    descripcion = forms.CharField(max_length=100, label="Descripcion del rol") #Descripcion del rol
    permisos = forms.ModelMultipleChoiceField( #Permisos que se le seran asignados a dicho rol
        queryset=Permisos.objects.all(), label="Permisos",
        help_text="Seleccione los Permisos.")

    class Meta:
        model = RolProyecto
        fields = ["nombre", "descripcion", "permisos"]


class FormTiposUS(forms.Form):
    nombre = forms.CharField(max_length=100) #Nombre del Tipo de User Story
    prefijo = forms.CharField(max_length=5) #Prefijo que se le sera asignado


class FormEstadoUS(forms.Form):
    nombre = forms.CharField(max_length=100) #Nombre de Estado del User Story


class FormUS(ModelForm):

    prioridad_de_negocio = forms.IntegerField(min_value=1, max_value=10, label="Prioridad de negocio") #Prioridad de negocio para el US
    prioridad_tecnica = forms.IntegerField(min_value=1, max_value=10, label="Prioridad tecnica") #Prioridad tecnica para el US
    duracion = forms.IntegerField(label="Tiempo estimado en horas.")

    class Meta:
        model = UserStory #Campos para nombre, descripcion, tipo, prioridad de negocio, prioridad de tecnica y la duracion que tendra
        fields = ["nombre", "descripcion", "tipo", "prioridad_de_negocio", "prioridad_tecnica", "duracion"]


class FormSprint(ModelForm):

    duracion = forms.IntegerField(min_value=1, max_value=30, label="Duracion del sprint en dias habiles", required=True)#Duracion del Sprint

    class Meta:
        model = Sprint
        fields = ["descripcion", "duracion"]#Campos para la descripcion y la duracion


class FormFeriado(ModelForm):

    fecha = forms.DateField(label="Ingrese la fecha del feriado.", required=True)

    class Meta:
        model = Feriado
        fields = ["fecha", "nombre"]


class FormMiembroSprint(ModelForm):

    carga_horaria = forms.IntegerField(min_value=1, max_value=12, label="Carga horaria",
                                       help_text="Cantidad de horas que el miembro puede trabajar por dia") #Carga horaria asignada para trabajar por dia

    class Meta:
        model = MiembrosSprint
        fields = ["miembro", "carga_horaria"] #Campo para los miembros y la carga horaria respectiva


class FormUSSprint(forms.Form):
    user_stories = forms.ModelMultipleChoiceField(queryset=UserStory.objects.all(), label="US a ingresar al Sprint.",
                                                  help_text="Seleccione al User Story que entrara al sprint.",) #Se elegira que User Story entrara al Sprint


class FormImportarMainPage(forms.Form):
    ACCIONES_CHOICES = (
        ("1", "Importar Roles"),
        ("2", "Importar Tipos de User Story"),
    )

    acciones = forms.ChoiceField(required=True, choices=ACCIONES_CHOICES, label="Accion a realizar:") #Accion a realizar
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), label="Proyecto del cual importar:") #Proyecto que sera importado


class FormImportarRolesProyecto(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=RolProyecto.objects.all(), label="Roles a importar:") #Se importan los roles del proyecto


class FormImportarTiposDeUS(forms.Form):
    tipos = forms.ModelMultipleChoiceField(queryset=TipoUserStory.objects.all(), #Se importan los tipos de User Story
                                           label="Tipos de User Story a importar:")


class FormAsignarDevAUserStory(forms.Form):
    desarrollador = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Seleccione el desarrollador.", required=False)#Se asigna un desarrollador al US


class FormAgregarTrabajoUS(ModelForm):

    log = forms.CharField(max_length=1000, label="Describa su trabajo realizado") #Describir el trabajo
    horas_trabajadas = forms.IntegerField(min_value=1, label="Cantidad de horas usadas.")#Horas que trabajara
    archivos = forms.FileField(label="Suba los archivos que verifiquen el trabajo realizado", required=True)#Archivos que validen dicho trabajo realizado

    class Meta:
        model = HistorialUS
        fields = ["log", "horas_trabajadas", "archivos"]#Campos de descripcion del trabajo, horas trabajadas y archivos


class FormAsignarRolAUsuario(forms.Form):

    roles = forms.ModelMultipleChoiceField(queryset=RolProyecto.objects.all(), #Se asigna rol al usuario
                                           label="Seleccione los roles para el usuario")


class FormSolicitarAprobacion(ModelForm):

    descripcion_del_trabajo = forms.CharField(max_length=1000, label="Describa su trabajo realizado")
    archivos = forms.FileField(label="Suba los archivos que verifiquen el trabajo realizado", required=True)

    class Meta:
        model = AprobacionDeUS
        fields = ["descripcion_del_trabajo", "archivos"]


class FormRechazarSolicitud(ModelForm):

    razon_de_rechazo = forms.CharField(max_length=1000, label="Describa la razón para rechazar esta solicitud")

    class Meta:
        model = AprobacionDeUS
        fields = ["razon_de_rechazo",]
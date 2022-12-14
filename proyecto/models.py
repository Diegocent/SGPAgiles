from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from Usuario.models import Usuario
from datetime import datetime, timedelta
# Create your models here.


class Equipo(models.Model):
    """
    Una clase utilizada para representar a un Equipo

    Atributos
    ---------
    nombre : str
        El nombre del equipo.
    miembros : ManyToManyField(Usuario)
        Miembros del equipo (Usuarios del sistema)
    """
    nombre = models.CharField(max_length=32, null=True)
    miembros = models.ManyToManyField(Usuario)

    def __str__(self):
        return '{}'.format(self.nombre)


class EstadoProyecto(models.TextChoices):
    NO_INICIADO = 'NO_INICIADO', 'No iniciado'
    EN_PROCESO = 'EN_PROCESO', 'En progreso'
    TERMINADO = 'TERMINADO', 'Terminado'
    CANCELADO = 'CANCELLED', 'Cancelado'
    RETRASADO = 'RETRASADO', 'Retrasado'


class Proyecto(models.Model):
    """
    Una clase utilizada para representar a un Proyecto

    Atributos
    ---------
    nombre : str
        El nombre del proyecto.
    descripcion : str
        Descripcion del Proyecto
    equipo : Equipo
        Objeto que agrupa a los miembros del proyecto. El Scrum Master forma parte del equipo por default.
    fecha_inicio: Date
        Fecha de inicio del proyecto
    fecha_fin_estimada: Date
        Fecha estimada del fin del proyecto.
    fecha_fin_real: Date
        Fecha real del fin del proyecto.
    estado: EstadoProyecto
        Estado del proyecto.
    scrum_master: Usuario
        Scrum Master del proyecto.

    Metodos
    -------
    obtener_tipos_de_user_story_del_proyecto()
        Devuelve los tipos de User Stories que estan asociados al proyecto

    tiene_user_stories_sin_terminar()
        Devuelve True si el proyecto tiene user stories sin terminar, False en caso contrario

    tiene_user_stories()
        Devuelve True si el proyecto tiene user stories, False en caso contrario

    tiene_un_equipo()
        Devuelve True si el proyecto tiene mas de un miembro en el equipo, False en caso contrario

    ya_termino()
        Devuelve True si el proyecto tiene el estado TERMINADO, False en caso contrario.
    """
    nombre = models.CharField(max_length=32)
    descripcion = models.CharField(max_length=500)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin_estimada = models.DateField(null=True)
    fecha_fin_real = models.DateField(null=True)
    estado = models.CharField(choices=EstadoProyecto.choices, max_length=100)
    scrum_master = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="scrum_master", null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def obtener_tipos_de_user_story_del_proyecto(self):
        return TipoUserStory.objects.filter(proyecto=self)

    def tiene_user_stories_sin_terminar(self):
        user_stories = UserStory.objects.filter(proyecto=self)
        user_stories = [us for us in user_stories if not us.finalizado]
        return len(user_stories) != 0

    def tiene_user_stories(self):
        user_stories = UserStory.objects.filter(proyecto=self)
        return len(user_stories) != 0

    def tiene_un_equipo(self):
        miembros = self.equipo.miembros.all()
        return len(miembros) > 1

    @staticmethod
    def ya_termino(id_proyecto):
        proyecto = Proyecto.objects.get(id=id_proyecto)
        return proyecto.estado == EstadoProyecto.TERMINADO


class EstadoSprint(models.TextChoices):
    NO_INICIADO = 'NO_INICIADO', 'No iniciado'
    EN_PROCESO = 'EN_PROCESO', 'En progreso'
    TERMINADO = 'TERMINADO', 'Terminado'
    CANCELADO = 'CANCELADO', 'Cancelado'


class Sprint(models.Model):
    """
       Una clase utilizada para representar a un Sprint

       Atributos
       ---------
       nombre : str
           El nombre del Sprint.
       descripcion : str
           Descripcion del Sprint
       proyecto : Proyecto
           Proyecto al cual el sprint esta asociado.
       fecha_inicio: Date
           Fecha de inicio del proyecto
       fecha_fin_estimada: Date
           Fecha estimada del fin del sprint.
       fecha_fin: Date
           Fecha real del fin del sprint.
       estado: EstadoSprint
           Estado del Sprint.
       duracion: int
           Duracion en dias del sprint.
        capacidad_usada: int
            Capacidad usada del sprint en horas.

       Metodos
       -------
       obtener_ultimo_valor_de_sprint()
           Devuelve el ultimo numero asignado a un sprint de un proyecto en especifico (no es el id del objeto)

       tiene_miembros()
           Devuelve True si el sprint tiene miembros asignados, False en caso contrario

       capacidad() - property
           Calcula la capacidad del sprint haciendo la suma de la capacidad individual de cada miembro del sprint

       calcular_capacidad_usada()
           Calcula la capacidad usada del sprint haciendo la suma de la duracion individual
           de cada US del sprint y lo guarda en disco.

       tiene_user_stories()
            Devuelve True si el proyecto tiene user stories, False en caso contrario

        hay_otros_sprints_en_proceso()
            Devuelve True si el proyecto tiene otros sprints en proceso, False en caso contrario

        hay_otros_sprints_en_proceso()
            Devuelve True si el proyecto tiene otros sprints en proceso, False en caso contrario

        obtener_sprint_en_proceso()
            Devuelve el sprint que esta en proceso actualmente

        obtener_user_stories_del_sprint()
            Devuelve los user stories asignados al sprint

        hay_otros_sprints_en_planificacion()
           Devuelve True si el proyecto tiene otros sprints en planificacion, False en caso contrario

        calcular_fecha_fin_estimada()
            Calcula la fecha fin estimada del sprint. Usado para la generacion del burndown chart.


       """
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    fecha_fin_estimada = models.DateField(null=True)
    estado = models.CharField(choices=EstadoProyecto.choices, max_length=100)
    duracion = models.IntegerField(null=True, verbose_name='Duraci??n en d??as')
    capacidad_usada = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Sprint {}'.format(self.numero)

    @staticmethod
    def obtener_ultimo_valor_de_sprint(id_proyecto):
        ultimo_valor = Sprint.objects.all().filter(proyecto_id=id_proyecto).last()
        if ultimo_valor is not None:
            return ultimo_valor.numero + 1
        else:
            return 1

    @property
    def tiene_miembros(self):
        miembros = MiembrosSprint.objects.filter(sprint=self)
        if len(miembros) == 0:
            return False
        return True

    @property
    def capacidad(self):
        miembros = MiembrosSprint.objects.filter(sprint=self)
        capacidad = 0
        for miembro in miembros:
            capacidad += miembro.capacidad
        return capacidad


    def calcular_capacidad_usada(self):
        user_stories = UserStory.objects.filter(sprint=self)
        capacidad_usada = 0
        for us in user_stories:
            capacidad_usada += us.duracion
        self.capacidad_usada = capacidad_usada
        self.save()

    @property
    def tiene_user_stories(self):
        user_stories = UserStory.objects.filter(sprint=self)
        if len(user_stories) == 0:
            return False
        return True

    @staticmethod
    def hay_otros_sprints_en_proceso(id_proyecto):
        sprints_en_proceso = Sprint.objects.filter(estado=EstadoSprint.EN_PROCESO, proyecto_id=id_proyecto)
        if len(sprints_en_proceso) == 0:
            return False
        return True

    @staticmethod
    def obtener_sprint_en_proceso(id_proyecto):
        try:
            sprint_en_proceso = Sprint.objects.get(estado=EstadoSprint.EN_PROCESO, proyecto_id=id_proyecto)
            return sprint_en_proceso
        except ObjectDoesNotExist:
            return None

    def obtener_user_stories_del_sprint(self):
        return UserStory.objects.filter(sprint=self)

    @staticmethod
    def hay_otros_sprints_en_planificacion(id_proyecto):
        sprints_en_planificacion = Sprint.objects.filter(estado=EstadoSprint.NO_INICIADO, proyecto_id=id_proyecto)
        if len(sprints_en_planificacion) == 0:
            return False
        return True

    def calcular_fecha_fin_estimada(self):
        fecha_fin = self.fecha_inicio
        feriados = Feriado.objects.filter(proyecto=self.proyecto).values_list("fecha", flat=True)
        dias_habiles = 0

        while dias_habiles < self.duracion:
            es_feriado = fecha_fin in feriados
            es_finde = fecha_fin.weekday() >= 5

            if not es_feriado and not es_finde:
                dias_habiles += 1

            fecha_fin += timedelta(days=1)

        self.fecha_fin_estimada = fecha_fin
        self.save()


class MiembrosSprint(models.Model):
    """
   Una clase utilizada para representar a un Sprint

   Atributos
   ---------
   sprint : Sprint
       El Sprint al que esta asociada el miembro
   miembro : Usuario
       El usuario asignado al sprint
   carga_horaria : int
       Cantidad de horas por dia que el miembro puede trabajar
    capacidad : int
       Carga horaria al miembro * duracion del sprint

    """
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    miembro = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carga_horaria = models.PositiveIntegerField() #cantidad de horas por dia que el miembro puede trabajar
    capacidad = models.PositiveIntegerField() #carga horaria al miembro * duracion del sprint

    def __str__(self):
        return 'Miembro del Sprint {} - {}'.format(self.sprint.numero, self.miembro.username)


class TipoUserStory(models.Model):
    """
    Clase utilizada para representar a un Tipo de User Story

    Atributos
    ---------

    nombre: str
        El nombre del Tipo de User Story.
    prefijo: str
        El prefijo del Tipo de User Story. Se agrega al codigo del User Story
    proyecto: Proyecto
        El proyecto del Tipo de User Story.
    """
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=5)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class OrdenEstado(models.Model):
    """
    Una clase para el orden de un estado de tipo de user story

    Atributos
    ---------

    orden: int
        representacion de la orden en un entero

    Metodos
    -------
    obtener_ultimo_valor_de_sprint()
        Devuelve el ultimo numero asignado a un orden ya existente (no es el id del objeto).


    """
    orden = models.PositiveIntegerField()

    @staticmethod
    def obtener_ultimo_valor_de_orden(tipo_id):
        ultimo_valor = OrdenEstado.objects.all().filter(orden_del_estado__tipoUserStory_id=tipo_id).first()
        if ultimo_valor is None:
            return 1
        return ultimo_valor.orden + 1

    class Meta:
        ordering = ["-orden"]


class EstadoUS(models.Model):
    """
    Una clase utilizada para representar el estado de un User Story. Tambien usado para el nombre
    de las columnas del Kanban

    Atributos
    ---------
    nombre: str
        Nombre del estado
    orden: Orden
        Orden asociado del estado. (utilizado para organizar el Kanban).
    tipoUserStory: TipoUserStory
        El tipo del User Story al cual pertenece el estado.

    """
    nombre = models.CharField(max_length=100)
    orden = models.ForeignKey(OrdenEstado, on_delete=models.CASCADE, related_name="orden_del_estado")
    tipoUserStory = models.ForeignKey(TipoUserStory, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        ordering = ["-orden"]


class Prioridad(models.TextChoices):
    ALTA = 'ALTA', 'Alta'
    MEDIA = 'MEDIA', 'Media'
    BAJA = 'BAJA', 'Baja'


class UserStory(models.Model):
    """
    Clase utilizada para representar a un User Story (US)

    Atributos
    ---------

    numero: int
        Entero utilizado para generar el codigo del User Story
    aprobado_por_scrum_master: bool
        Booleano utilizado para saber si el US fue aprobado por el user story
    proyecto: Proyecto
        Proyecto al cual fue asignado el US
    sprint: Sprint
        Sprint al cual fue asignado el US
    nombre: str
    descripcion: str
    tipo: TipoUserStory
        Tipo del User Story
    estado: EstadoUS
        Estado actual del User Story. default: TO DO
    prioridad: int
        Prioridad del US. Calculado usando la prioridad tecnica, la de negocio y el esfuerzo anterior.
    duracion: int
        Cuantas horas se estima que se tardaria en terminar el US.
    desarrollador: Usuario
        Usuario encargado de trabajar en el US

    Metodos
    -------

    calcular_prioridad()
        Funcion utilizada para calcular la prioridad del US usando la prioridad
        de negocio, la prioridad tecnica y el esfuerzo anterior.

    codigo()
        propiedad utilizada para generar el codigo del US concatenando el prefijo
        de su tipo con el numero del US.

    total_horas_trabajadas()
        Propiedad utilizada para calcular las horas trabajadas del US.

    obtener_ultimo_valor_de_us()
        Funcion utilizada para obtener el ultimo numero asignado a un US de un
        proyecto en especifico.

    finalizado()
        Funcion que devuelve un True en caso de que el estado del US sea DONE, False en caso contrario.

    """
    numero = models.PositiveIntegerField(default=0)
    aprobado_por_scrum_master = models.BooleanField(default=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    tipo = models.ForeignKey(TipoUserStory, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoUS, on_delete=models.CASCADE, null=True)
    prioridad = models.PositiveIntegerField(default=0)
    prioridad_de_negocio = models.PositiveIntegerField()
    prioridad_tecnica = models.PositiveIntegerField()
    esfuerzo_anterior = models.PositiveIntegerField(default=0)
    duracion = models.PositiveIntegerField()
    desarrollador = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

    def calcular_prioridad(self):
        self.prioridad = round(0.6 * self.prioridad_de_negocio + 0.5 * self.prioridad_tecnica + self.esfuerzo_anterior)
        self.save()

    @property
    def codigo(self):
        return self.tipo.prefijo + " - US" + "{}".format(self.numero)

    @property
    def total_horas_trabajadas(self):
        historiales = HistorialUS.objects.filter(user_story_id=self.id)
        total_horas = 0
        for historia in historiales:
            total_horas += historia.horas_trabajadas
        return total_horas

    @staticmethod
    def obtener_ultimo_valor_de_us(id_proyecto):
        ultimo_valor = UserStory.objects.all().filter(proyecto_id=id_proyecto).last()
        if ultimo_valor is not None:
            return ultimo_valor.numero + 1
        else:
            return 1

    @property
    def finalizado(self):
        if self.estado.nombre == "DONE":
            return True
        else:
            return False


    class Meta:
        ordering = ["-prioridad"]


class HistorialUS(models.Model):
    """
    Funcion donde se almacena toda la actividad realizada en el US.

    Atributos
    ---------

    user_story: UserStory
        User Story al cual corresponde el historial.
    sprint: Sprint
        Sprint al cual esta asociado un entry del historial. (Usado para
        saber en cual sprint se realizo un trabajo en particular)
    log: str
        Descripcion del trabajo realizado por el user o de manera automatica por el sistema.
    horas_trabajadas: int
        En caso de que el user cargue un trabajo, debe agregar cuantas horas utilizo para el trabajo.
    fecha: Date
        fecha del trabajo o accion realizada al US.
    usuario: Usuario
        Quien realizo el trabajo o la accion realizada al US.
    archivos: File
        Archivo cargado por el user para evidenciar el trabajo realizado
    """
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    log = models.CharField(max_length=1000)
    horas_trabajadas = models.PositiveIntegerField(default=0)
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivos = models.FileField(null=True, upload_to="historial", default="0")

    class Meta:
        ordering = ["fecha", "id"]


class EstadoAprobacion(models.TextChoices):
    EN_ESPERA = 'EN_ESPERA', 'En espera de aprobacion'
    RECHAZADO = 'RECHAZADO', 'Rechazado'
    ACEPTADO = 'ACEPTADO', 'Aceptado'


class AprobacionDeUS(models.Model):
    """
    Clase para solicitar la aprobacion del US.

    Atributos
    ---------

    numero: int
        Numero de la solicitud
    user_story: UserStory
        User Story al cual se realiza la solicitud de aprobacion
    descripcion_del_trabajo: str
        descripcion mas general del trabajo realizado.
    fecha: Date
        Fecha de cuando se realizo la solicitud
    solicitado_por: Usuario
        Usuario que solicito la aprobacion del US.
    aprobado_por: Usuario
        Usuario que aprobo el US.
    estado: str
        Estado de la solicitud.
    razon_de_rechazo: str
        Razon por la cual la solicitud fue rechazada.

    Metodos
    -------

    obtener_ultimo_valor_de_solicitud()
        Funcion para obtener el ultimo numero de solicitud de un US en especifico.
    """
    numero = models.PositiveIntegerField(default=0)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    descripcion_del_trabajo = models.CharField(max_length=1000)
    fecha = models.DateField()
    solicitado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="desarrollador")
    archivos = models.FileField(null=True, upload_to="historial", default="0")
    aprobado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="aprobado_por", null=True)
    estado = models.CharField(choices=EstadoAprobacion.choices, max_length=100, default=EstadoAprobacion.EN_ESPERA)
    razon_de_rechazo = models.CharField(max_length=1000, null=True)

    @staticmethod
    def obtener_ultimo_valor_de_solicitud(id_us):
        ultimo_valor = AprobacionDeUS.objects.all().filter(user_story_id=id_us).last()
        if ultimo_valor is not None:
            return ultimo_valor.numero + 1
        else:
            return 1


class Feriado(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

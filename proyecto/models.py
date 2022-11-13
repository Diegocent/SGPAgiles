from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from Usuario.models import Usuario
# Create your models here.


class Equipo(models.Model):
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


class EstadoSprint(models.TextChoices):
    NO_INICIADO = 'NO_INICIADO', 'No iniciado'
    EN_PROCESO = 'EN_PROCESO', 'En progreso'
    TERMINADO = 'TERMINADO', 'Terminado'
    CANCELADO = 'CANCELADO', 'Cancelado'


class Sprint(models.Model):
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    estado = models.CharField(choices=EstadoProyecto.choices, max_length=100)
    duracion = models.IntegerField(null=True, verbose_name='Duración en días')

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

    @property
    def capacidad_usada(self):
        user_stories = UserStory.objects.filter(sprint=self)
        capacidad_usada = 0
        for us in user_stories:
            capacidad_usada += us.duracion
        return capacidad_usada

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


class MiembrosSprint(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    miembro = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carga_horaria = models.PositiveIntegerField() #cantidad de horas por dia que el miembro puede trabajar
    capacidad = models.PositiveIntegerField() #carga horaria al miembro * duracion del sprint

    def __str__(self):
        return 'Miembro del Sprint {} - {}'.format(self.sprint.numero, self.miembro.username)


class TipoUserStory(models.Model):
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=5)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class OrdenEstado(models.Model):
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
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
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
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
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin_estimada = models.DateTimeField(null=True)
    fecha_fin_real = models.DateTimeField(null=True)
    estado = models.CharField(choices=EstadoProyecto.choices, max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class EstadoSprint(models.TextChoices):
    NO_INICIADO = 'NO_INICIADO', 'No iniciado'
    EN_PROCESO = 'EN_PROCESO', 'En progreso'
    TERMINADO = 'TERMINADO', 'Terminado'


class Sprint(models.Model):
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    estado = models.CharField(choices=EstadoProyecto.choices, max_length=100)

    def __str__(self):
        return '{}'.format(self.numero)


class TipoUserStory(models.Model):
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=5)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class OrdenEstado(models.Model):
    orden = models.PositiveIntegerField()

    def obtener_ultimo_valor_de_orden(tipo_id):
        ultimo_valor = OrdenEstado.objects.all().filter(orden_del_estado__tipoUserStory_id=tipo_id).first()
        return ultimo_valor.orden + 1

    class Meta:
        ordering = ["-orden"]


class EstadoUS(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.ForeignKey(OrdenEstado, on_delete=models.CASCADE, related_name="orden_del_estado")
    tipoUserStory = models.ForeignKey(TipoUserStory, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


class Prioridad(models.TextChoices):
    ALTA = 'ALTA', 'Alta'
    MEDIA = 'MEDIA', 'Media'
    BAJA = 'BAJA', 'Baja'


class UserStory(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    tipo = models.ForeignKey(TipoUserStory, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoUS, on_delete=models.CASCADE, null=True)
    prioridad = models.PositiveIntegerField()
    prioridad_de_negocio = models.PositiveIntegerField()
    prioridad_tecnica = models.PositiveIntegerField()
    duracion = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.nombre)
from django.db import models
from Usuario.models import Usuario
# Create your models here.


class Equipo(models.Model):
    nombre = models.CharField(max_length=32)
    miembros = models.ManyToManyField(Usuario)


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

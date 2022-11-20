from django.db import models
from proyecto.models import Usuario


# Create your models here.
class Notificacion(models.Model):
    leido = models.BooleanField(default=False)
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    url = models.CharField(null=True, max_length=150)

    @staticmethod
    def obtener_notificacion_de_usuario(usuario):
        return Notificacion.objects.filter(leido=False, usuario=usuario)

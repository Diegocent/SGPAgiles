from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class Permisos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class RolSistema(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permisos)

    def __str__(self):
        return '{}'.format(self.nombre)


class RolProyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permisos)
    proyecto = models.ForeignKey("proyecto.Proyecto", on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)


# Create your models here.
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100, default="desconocido")
    username = None
    password = None
    email = models.EmailField(unique=True)
    rolSistema = models.ManyToManyField(RolSistema)
    rolProyecto = models.ManyToManyField(RolProyecto)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuario_custom_sgpa'

    def es_admin(self):
        try:
            admin = self.rolSistema.get(nombre="admin")
            return True
        except ObjectDoesNotExist:
            return False

    def es_scrum_master(self, id_proyecto):
        try:
            scrum = self.rolProyecto.get(nombre="scrum master", proyecto=id_proyecto)
            return True
        except ObjectDoesNotExist:
            return False

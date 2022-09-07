from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager


class Permisos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)


class RolSistema(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permisos)


class RolProyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permisos)
    proyecto = models.ForeignKey("proyecto.Proyecto", on_delete=models.CASCADE)


# Create your models here.
class Usuario(AbstractBaseUser):
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

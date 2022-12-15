from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class Permisos(models.Model):
    """
    Clase que representa a un permiso

    Atributos
    ---------
    nombre : str
           El nombre del permiso
    descripcion : str
           El nombre del permiso
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)


class RolSistema(models.Model):
    """
    Clase que representa a un rol de sistema

    Atributos
    ---------
    nombre : str
           El nombre del rol de sistema
    descripcion : str
           El nombre del rol de sistema
    permiso : permisos
        Una lista de los permisos que pertenecen al rol
    """
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

    def agregar_permisos(self, permisos):
        permisos_objects = Permisos.objects.all().filter(nombre__in=permisos)
        self.permisos.add(*permisos_objects)


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
            scrum = self.rolProyecto.get(nombre="Scrum Master", proyecto=id_proyecto)
            return True
        except ObjectDoesNotExist:
            return False

    def tiene_permisos(self, permisos: list, id_proyecto=0):
        tiene_permisos = False
        for permiso in permisos:
            encontro_permiso = False
            roles = self.rolSistema.all()
            for rol in roles:
                try:
                    rol.permisos.get(nombre=permiso)
                    encontro_permiso = True
                    break
                except ObjectDoesNotExist:
                    rolesProyecto = self.rolProyecto.all().filter(proyecto_id=id_proyecto)
                    for rolproyecto in rolesProyecto:
                        try:
                            rolproyecto.permisos.get(nombre=permiso)
                            encontro_permiso = True
                            break
                        except ObjectDoesNotExist:
                            pass
            if encontro_permiso:
                tiene_permisos = True
                break
        return tiene_permisos


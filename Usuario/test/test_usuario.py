from django.core.exceptions import ObjectDoesNotExist

from Usuario.models import Usuario, RolSistema, Permisos, RolProyecto
import pytest, pytz
from datetime import datetime


# test creado el dia 28/08/2022 por Carin Martinez
from proyecto.models import Proyecto, EstadoProyecto


def funcion(x):
    return x+2

def test_usuario():
    x = 5
    assert funcion(3) == x, "ERROR: 3+2 != {}".format(x)

@pytest.mark.django_db
#test creado el dia 5/09/2022 por Marcelo Molas
def test_crear_usuario():
    Usuario.objects.create_user("prueba@a.a")
    usuarios = Usuario.objects.all()
    assert(len(usuarios) == 1), "ERROR: Usuario no pudo crearse correctamente"

@pytest.mark.django_db
def test_verificar_si_es_admin():
    user = Usuario.objects.create_user("prueba@a.a")
    rol_a_guardar = RolSistema.objects.create(nombre="admin", descripcion="Admin del sistema")
    user.rolSistema.add(rol_a_guardar)
    try:
        rol = user.rolSistema.get(nombre="admin")
    except:
        raise Exception("ERROR, El usuario no cuenta con el rol ADMIN.")


def tiene_permisos(user: Usuario, permisos: list):
    tiene_permisos = True
    for permiso in permisos:
        encontro_permiso = True
        roles = user.rolSistema.all()
        for rol in roles:
            try:
                rol.permisos.get(nombre=permiso)
            except ObjectDoesNotExist:
                rolesProyecto = user.rolProyecto.all()
                for rolproyecto in rolesProyecto:
                    try:
                        rolproyecto.permisos.get(nombre=permiso)
                    except ObjectDoesNotExist:
                        encontro_permiso = False
                        break
                if not encontro_permiso or len(rolesProyecto) == 0:
                    encontro_permiso = False
                    break
        if not encontro_permiso or len(roles) == 0:
            tiene_permisos = False
            break
    return tiene_permisos

@pytest.mark.django_db
def test_verificar_si_tiene_permiso():
    user = Usuario.objects.create_user("prueba@a.a")
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    permiso = Permisos.objects.create(nombre="TEST", descripcion="TEST")
    permisoProy = Permisos.objects.create(nombre="TEST2", descripcion="TEST")

    rol_a_guardar = RolSistema.objects.create(nombre="admin", descripcion="Admin del sistema")
    rolp_a_guardar = RolProyecto.objects.create(nombre="developer", descripcion="Desarrollador del proyecto", proyecto=proyecto)

    rol_a_guardar.permisos.add(permiso)
    rolp_a_guardar.permisos.add(permisoProy)

    user.rolSistema.add(rol_a_guardar)
    user.rolProyecto.add(rolp_a_guardar)
    if not tiene_permisos(user, ["TEST2", "TEST"]):
        raise Exception("El usuario no tiene el permiso requerido.")

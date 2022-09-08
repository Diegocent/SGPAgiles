from Usuario.models import Usuario, RolSistema
import pytest


# test creado el dia 28/08/2022 por Carin Martinez
def funcion(x):
    return x+2

def test_usuario():
    assert funcion(3) == 5

@pytest.mark.django_db
#test creado el dia 5/09/2022 por Marcelo Molas
def test_crear_usuario():
    Usuario.objects.create_user("prueba@a.a")
    usuarios = Usuario.objects.all()
    assert(len(usuarios) == 1)

@pytest.mark.django_db
def test_verificar_si_es_admin():
    user = Usuario.objects.create_user("prueba@a.a")
    rol_a_guardar = RolSistema.objects.create(nombre="admin", descripcion="Admin del sistema")
    user.rolSistema.add(rol_a_guardar)
    rol = user.rolSistema.get(nombre="admin")
    assert rol

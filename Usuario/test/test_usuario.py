from Usuario.models import Usuario, RolSistema
import pytest


# test creado el dia 28/08/2022 por Carin Martinez
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


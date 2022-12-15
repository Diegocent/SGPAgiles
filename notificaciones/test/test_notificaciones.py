
from Usuario.models import Usuario
from notificaciones.models import Notificacion
import pytest, pytz

def funcion(x):
    return x+1

@pytest.mark.django_db
def test_notificacion_obtener():
    user = Usuario.objects.create_user("prueba@a.a")
    notificaciones = Notificacion.objects.filter(usuario=user).order_by("-timestamp")
    assert len(notificaciones) == 0, "La lista no esta vacia, no deberia de haber ninguna notificacion en este punto"


@pytest.mark.django_db
def test_notificacion_crear_notificacion_para_usuario():
    user = Usuario.objects.create_user("prueba@a.a")
    Notificacion.objects.create(
        mensaje="Notificaciones de prueba para el usuario '{}'".format(user.email),
        usuario=user,
        url="/proyecto/"
    )
    notificaciones = Notificacion.objects.filter(usuario=user).order_by("-timestamp")

    assert len(notificaciones) == 1, "La lista esta vacia, No se creo la notificacion correctamente"
    for notifcacion in notificaciones:
        assert notifcacion.mensaje == "Notificaciones de prueba para el usuario 'prueba@a.a'", \
            "El mensaje de la notificacion no contiene el mail del usuario que debe de tener."


@pytest.mark.django_db
def test_notificacion_crear_notificacion_para_usuario_y_leer():
    user = Usuario.objects.create_user("prueba@a.a")
    Notificacion.objects.create(
        mensaje="Notificaciones de prueba para el usuario '{}'".format(user.email),
        usuario=user,
        url="/proyecto/"
    )
    notificaciones = Notificacion.objects.filter(usuario=user).order_by("-timestamp")

    assert len(notificaciones) == 1, "La lista esta vacia, No se creo la notificacion correctamente"
    for notifcacion in notificaciones:
        assert notifcacion.mensaje == "Notificaciones de prueba para el usuario 'prueba2@a.a'", \
            "El mensaje de la notificacion no contiene el mail del usuario que debe de tener."
        notifcacion.leido = True
        notifcacion.save()
        assert notifcacion.leido, "La notificacion fue leida pero no aparece como leida"
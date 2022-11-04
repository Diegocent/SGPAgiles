import pytest, pytz
from proyecto.models import Proyecto, EstadoProyecto, UserStory, TipoUserStory, EstadoUS, OrdenEstado, AprobacionDeUS, \
    EstadoAprobacion
from Usuario.models import Usuario
from datetime import date, datetime


# test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_proyecto():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )
    proyectos = Proyecto.objects.all()
    assert len(proyectos) == 1, "ERROR: Proyecto no fue creado."


# test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_tipouserstory():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)
    tipos = TipoUserStory.objects.all()
    assert len(tipos) == 1, "ERROR: Tipo de usuario no fue creado."


# test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_userstory():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)

    us = UserStory.objects.create(nombre="TEST-1", descripcion="TEST", tipo=tipo, proyecto=proyecto,
                                  prioridad_de_negocio=1, prioridad_tecnica=1, esfuerzo_anterior=0, duracion=10)

    userstories = UserStory.objects.all()
    assert len(userstories) == 1, "ERROR: User Story no fue creado."


# test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_estados_y_agregar_a_tipo():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)
    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1, "ERROR: Estado de US no fue creado."


# test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_sprint():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1, "ERROR: Sprint no fue creado."


@pytest.mark.django_db
def test_modificar_estado_US():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1, "ERROR al modificar el estado del US"


@pytest.mark.django_db
def test_cancelar_sprint():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1, "ERROR al cancelar un sprint."


@pytest.mark.django_db
def test_estimar_US():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1, "ERROR: US no pudo estimarse correctamente."


# hecho por Diego
@pytest.mark.django_db
def test_crear_solicitud():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)
    us = UserStory.objects.create(nombre="TEST-1", descripcion="TEST", tipo=tipo, proyecto=proyecto,
                                  prioridad_de_negocio=1, prioridad_tecnica=1, esfuerzo_anterior=0, duracion=10)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)
    usuario = Usuario.objects.create(email='a@a.a')
    AprobacionDeUS.objects.create(solicitado_por=usuario,
        descripcion_del_trabajo="descripcion_del_trabajo",
        archivos="archivos",
        user_story_id=us.id,
        fecha="2022-11-03",
        numero=AprobacionDeUS.obtener_ultimo_valor_de_solicitud(id_us=us.id)
    )
    aprobaciones = AprobacionDeUS.objects.all()
    assert len(aprobaciones) == 1, "ERROR: no se pudo aprobar la solicitud."


# hecho por Diego
@pytest.mark.django_db
def test_rechazar_solicitud():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                       descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12,
                                                                   tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12,
                                                             tzinfo=pytz.timezone("America/Asuncion")),
                                       )

    tipo = TipoUserStory.objects.create(nombre="test1", prefijo="TEST", proyecto=proyecto)
    us = UserStory.objects.create(nombre="TEST-1", descripcion="TEST", tipo=tipo, proyecto=proyecto,
                                  prioridad_de_negocio=1, prioridad_tecnica=1, esfuerzo_anterior=0, duracion=10)

    orden_1 = OrdenEstado.objects.create(orden=OrdenEstado.obtener_ultimo_valor_de_orden(tipo_id=tipo.id))
    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo, orden=orden_1)

    usuario = Usuario.objects.create(email='a@a.a')
    solicitud = AprobacionDeUS.objects.create(solicitado_por=usuario,
        descripcion_del_trabajo="descripcion_del_trabajo",
        archivos="archivos",
        user_story_id=us.id,
        fecha="2022-11-03",
        numero=AprobacionDeUS.obtener_ultimo_valor_de_solicitud(id_us=us.id)
    )
    solicitud.razon_de_rechazo = "razon_de_rechazo"
    solicitud.estado = EstadoAprobacion.RECHAZADO
    solicitud.save()
    assert solicitud.estado == "RECHAZADO", "ERROR: no se pudo rechazar la solicitud."

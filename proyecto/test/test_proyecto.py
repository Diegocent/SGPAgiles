import pytest, pytz
from proyecto.models import Proyecto, EstadoProyecto, UserStory, TipoUserStory, EstadoUS
from datetime import date, datetime

#test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_proyecto():
    proyecto = Proyecto.objects.create(nombre="ver_pagina_admin",
                                      descripcion="Permiso para ver la pagina del administrador",
                                       estado=EstadoProyecto.NO_INICIADO,
                                       fecha_fin_estimada=datetime(year=2023, month=9, day=12, hour=12, minute=12, tzinfo=pytz.timezone("America/Asuncion")),
                                       fecha_inicio=datetime(year=2022, month=9, day=12, hour=12, minute=12, tzinfo=pytz.timezone("America/Asuncion")),
                                       )
    proyectos = Proyecto.objects.all()
    assert len(proyectos) == 1

#test creado el dia 5/09/2022 por Marcelo Molas
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
    assert len(tipos) == 1

#test creado el dia 5/09/2022 por Marcelo Molas
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

    us=UserStory.objects.create(nombre="TEST-1",descripcion="TEST", tipo=tipo, proyecto=proyecto)

    userstories = UserStory.objects.all()
    assert len(userstories) == 1


#test creado el dia 5/09/2022 por Marcelo Molas
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

    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1
    
#test creado el dia 5/09/2022 por Marcelo Molas
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

    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1
    
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

    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1
    
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

    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1
    
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

    estado = EstadoUS.objects.create(nombre="TEST", tipoUserStory=tipo)

    estados = EstadoUS.objects.all()
    assert len(estados) == 1

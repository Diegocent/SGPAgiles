import pytest
from Usuario.models import RolSistema, Permisos

#test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_permisos():
    permiso = Permisos.objects.create(nombre="ver_pagina_admin",
                                      descripcion="Permiso para ver la pagina del administrador")
    permisos = Permisos.objects.all()
    assert len(permisos) == 1

#test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_crear_roles():
    rol = RolSistema.objects.create(nombre="admin", descripcion="Administrador del sistema")
    roles = RolSistema.objects.all()
    assert len(roles) == 1

#test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_asignar_permisos_a_rol():
    rol = RolSistema.objects.create(nombre="admin", descripcion="Administrador del sistema")
    permiso = Permisos.objects.create(nombre="ver_pagina_admin",
                                      descripcion="Permiso para ver la pagina del administrador")
    rol.permisos.add(permiso)

    permisos_del_rol = rol.permisos.all()
    assert len(permisos_del_rol) == 1

#test creado el dia 5/09/2022 por Marcelo Molas
@pytest.mark.django_db
def test_buscar_permiso_en_un_rol():
    rol = RolSistema.objects.create(nombre="admin", descripcion="Administrador del sistema")
    permiso = Permisos.objects.create(nombre="ver_pagina_admin",
                                      descripcion="Permiso para ver la pagina del administrador")
    rol.permisos.add(permiso)

    permiso_buscado = rol.permisos.get(nombre = "ver_pagina_admin")
    assert permiso_buscado.nombre == "ver_pagina_admin"


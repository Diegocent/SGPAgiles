from django import template
from django.urls import resolve, Resolver404
import re
from proyecto.models import Proyecto, TipoUserStory, UserStory, Sprint
from Usuario.models import RolProyecto, Usuario, RolSistema, Permisos

register = template.Library()


@register.inclusion_tag('herramientas/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    """

    """
    request = context['request']
    path:str = request.path

    names = {
        'proyecto': 'Proyectos',
        'tipoUS': 'Tipos de User Story',
        'user-story': 'Historia de Usuario',
        'sprint': 'Sprint',
        'rol': 'Rol',
    }
    get_name = {
        'proyecto': lambda x: Proyecto.objects.get(pk=x).nombre,
        'tipoUS': lambda x: TipoUserStory.objects.get(pk=x).nombre,
        'user_story': lambda x: UserStory.objects.get(pk=x).nombre,
        'sprint': lambda x: Sprint.objects.get(pk=x).numero,
        'rol': lambda x: RolProyecto.objects.get(pk=x).nombre,
    }
    breadcrumb = []
    path_separado = path.split(sep="/")

    anterior = ""
    id_encontrado = False
    for pedazo in path_separado:
        if pedazo == "":
            continue
        print(pedazo)
        if re.match(r'[0-9]', pedazo):
            id_encontrado = True


        previous_path = breadcrumb[-1][1] if breadcrumb else ''

        if id_encontrado:
            name = names[anterior] if anterior in names else anterior
            model_name_id = get_name[anterior](pedazo) if anterior in get_name else pedazo
            id_encontrado = False


            model_url = f'{previous_path}/{pedazo}'


            breadcrumb.append((model_name_id, model_url, exists_path(model_url)))
        else:
            name = names[pedazo] if pedazo in names else pedazo
            model_list_url = f"{previous_path}/{pedazo}"
            breadcrumb.append((name, model_list_url, exists_path(model_list_url)))
        anterior = pedazo
    breadcrumb.insert(0, ('Home', '/', True))
    return {
        'breadcrumb': breadcrumb,
    }


def exists_path(path):
    """
    Retorna True si existe alguna vista que coincida con el path
    """
    try:
        resolve(f"{path}/")
        return True
    except Resolver404:
        return False

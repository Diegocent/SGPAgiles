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
    path = request.path

    names = {
        'proyectos': 'Proyecto',
        'tipo_user_story': 'Tipo de Historia de Usuario',
        'user-story': 'Historia de Usuario',
        'sprint': 'Sprint',
        'rol': 'Rol',
    }
    get_name = {
        'proyectos': lambda x: Proyecto.objects.get(pk=x).nombre,
        'tipo_user_story': lambda x: TipoUserStory.objects.get(pk=x).nombre,
        'user_story': lambda x: UserStory.objects.get(pk=x).nombre,
        'sprint': lambda x: Sprint.objects.get(pk=x).nombre,
        'rol': lambda x: RolProyecto.objects.get(pk=x).nombre,
    }
    breadcrumb = []
    while path:

        match = re.search(r'(?P<model_name>[\w-]+)/(?P<model_id>[\w-]+)/?', path)
        if not match:
            break
        path = path[match.end():]

        model_name = match.group('model_name')
        model_id = match.group('model_id')

        name = names[model_name] if model_name in names else model_name
        if model_id in ['create', 'edit', 'import', 'board']:
            model_name_id = names[model_id]
        else:
            model_name_id = get_name[model_name](model_id) if model_name in get_name else model_id

        model_url = f'{model_name}/{model_id}'
        previous_path = breadcrumb[-1][1] if breadcrumb else ''

        model_list_url = f"{previous_path}/{model_name}"
        model_id_url = f"{previous_path}/{model_url}"
        breadcrumb.append((name, model_list_url, exists_path(model_list_url)))
        breadcrumb.append((model_name_id, model_id_url, exists_path(model_id_url)))
    if(path):
        path = path.replace('/', '')
        previous_path = breadcrumb[-1][1] if breadcrumb else ''
        name = names[path] if path in names else path
        breadcrumb.append((name, f'{previous_path}/{path}', True))
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

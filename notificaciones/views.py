from django.shortcuts import render, redirect
from django.views import View
from Usuario.models import Usuario, RolProyecto
from .models import Notificacion


# Create your views here.
class NotificacionesPageView(View):

    def get(self, request):
        user: Usuario = request.user
        if user.is_authenticated:

            notificaciones_query = Notificacion.objects.filter(usuario=user).order_by("-timestamp")

            notificaciones = notificaciones_query[:10]

            for notificacion in notificaciones_query:
                if not notificacion.leido:
                    notificacion.leido = True
                    notificacion.save()

            context = {
                "notificaciones": notificaciones,
            }
            return render(request, 'herramientas/ver_mis_notificaciones.html', context)

        elif not user.is_authenticated:
            return redirect("home")

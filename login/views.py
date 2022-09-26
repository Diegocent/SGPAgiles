from django.http import HttpResponse
from django.shortcuts import render
from Usuario.models import Usuario


"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **login** - Funcion para hacer el login 
"""
# === login ===
def login(request):
        return render(request, 'index.html')


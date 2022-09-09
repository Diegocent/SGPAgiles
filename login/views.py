from django.http import HttpResponse
from django.shortcuts import render
from Usuario.models import Usuario


"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **login** - Funcion para hacer el login 
"""
def login(request):
    if not request.user.is_authenticated:
        return render(request,'account/login.html')
    else:
        return render(request,'index.html')

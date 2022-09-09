from django.http import HttpResponse
from django.shortcuts import render

"""
Todos los views para SGPAgiles 
Actualmente contamos con los siguientes views:

1. **login** - Funcion para hacer el login 
"""
def login(request):
    return render(request,'account/login.html')
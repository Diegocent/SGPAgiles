from django.http import HttpResponse
from django.shortcuts import render
from Usuario.models import Usuario


# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        return render(request,'account/login.html')
    else:
        return render(request,'index.html')

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from RFI.models import *


def index(request):
#    fondos=sw.objects.all().distinct('institucion')
    return render(request,'index.html',{})

def raiz(request):
    return render(request,'login.html',{})

def hall(request):
    return render(request,'hall.html',{})

def logout_(request):
    logout(request)
    return redirect('raiz')

from django.contrib.auth import authenticate,login
def login_(request):
    print('estoy en la vista login')
    usr = request.POST['usr']
    pasw = request.POST['pasw']
    user = authenticate(request,username = usr,password = pasw)
    if user is not None:
        login(request,user)
        print('pasó el login')
        return redirect('hall')
    else:
        print('error en el login')
        return redirect('raiz')


from django.shortcuts import render

def comite_rfl(request):
    return render(request,'rfl.html',{})

def arbitraje_rfl(request):
    return render(request,'rfl-arbitraje.html',{})
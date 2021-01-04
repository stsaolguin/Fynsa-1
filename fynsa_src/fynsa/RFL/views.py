from django.http import HttpResponse
from django.shortcuts import render
from RFL.formularios_RFL import *
import csv

def comite_rfl(request):
    return render(request,'rfl.html',{})

def arbitraje_rfl(request):
    fomulario_subida = lva_1()
    return render(request,'rfl-arbitraje.html',{'lva_1':fomulario_subida})

def llegada_rfl_1(request):
    if request.method=='POST':
        print('metodo POST')
        formularios = lva_1(request.POST,request.FILES)
        if formularios.is_valid():
            riskamerica = request.FILES['rsk']
            telerenta = request.FILES['tr']
            print('riskamerica,telerenta',riskamerica,telerenta)
            print('formulario valido')
            
            #archivo_abierto = open(telerenta,'r')
            #leer_csv = csv.reader(archivo_abierto,delimiter=';')
            #for r in leer_csv:
            #    print(r)


            return HttpResponse("Formulario Válido")
        
        print('formulario NO valido')
    
    return HttpResponse("Conectado")

def consulta_cintas(request):
    f_consulta_cintas = formulario_consulta_cintas()
    return render(request,'rfl-arbitraje-consultas.html',{'formulario_consulta_cintas':f_consulta_cintas})

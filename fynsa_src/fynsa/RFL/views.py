from django.http import HttpResponse
from django.shortcuts import render
from RFL.formularios_RFL import *
from RFL.funciones_externas_RFL import truncar
import io,csv
from RFL.models import tr,risk

def comite_rfl(request):
    return render(request,'rfl.html',{})

def arbitraje_rfl(request):
    fomulario_subida = lva_1()
    return render(request,'rfl-arbitraje.html',{'lva_1':fomulario_subida})

def llegada_rfl_1(request):
    if request.method=='POST':
        formularios = lva_1(request.POST,request.FILES)
        if formularios.is_valid():
            riskamerica = request.FILES['rsk']
            telerenta = request.FILES['tr']
            f_tr = io.TextIOWrapper(telerenta.file)
            f_rsk = io.TextIOWrapper(riskamerica.file)
            csv_tr = csv.DictReader(f_tr,delimiter=";")
            csv_rsk = csv.DictReader(f_rsk,delimiter=";")
            
            for r in csv_tr:
                a = r['Cantidad']
                b = a.split(',')[0]
                b = b.replace('.','')
                c = r['Duration']
                c = truncar(c,2)
                d = r['TIR Media']
                d = truncar(d,2)
                e = tr(instrumento=r['Instrumento'],cantidad=b,reajuste=r['Reaj.'],tir_media=d,duracion=c,tipo=r['Tipo'])
                e.save()
            for s in csv_rsk:
                nemo = s['Nemo']
                tipo = s['Tipo']
                riesgo = s['Riesgo']
                moneda = s['Moneda']
                monto_outstanding = s['Cantidad Out.']
                duracion = truncar(s['Duración'],2)
                tir = truncar(s['Tir Ult. Val.'],2)
                #print(nemo,tipo,riesgo,moneda,monto_outstanding,duracion,tir)
                f = risk(nemo=nemo,tipo=tipo,riesgo=riesgo,moneda=moneda,monto_outstanding=monto_outstanding,duracion=duracion,tir=tir)
                f.save()
            f_tr.close()
            f_rsk.close()
            return HttpResponse('vamos')
        
        print('formulario NO valido')
    
    return HttpResponse("Conectado")

def consulta_cintas(request):
    f_consulta_cintas = formulario_consulta_cintas()
    return render(request,'rfl-arbitraje-consultas.html',{'formulario_consulta_cintas':f_consulta_cintas})


def consulta_cintas_proceso(request):
    
    categoria = request.GET.get('categoria')
    rating = request.GET.get('rating')
    moneda = request.GET.get('moneda')
    duracion_inicial = request.GET.get('duracion_inicial')
    duracion_final = request.GET.get('duracion_final')
    
    print(categoria, 
    rating, 
    moneda, 
    duracion_inicial, 
    duracion_final)
    return HttpResponse('pasamos')
    
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from RFL.formularios_RFL import *
from RFL.funciones_externas_RFL import truncar,actualiza_riesgo,actualiza_tipo,limpia_risk
import io,csv,re
from RFL.models import tr,risk


def comite_rfl(request):
    return render(request,'rfl.html',{})

def arbitraje_rfl(request):
    fomulario_subida = lva_1_2()
    f_posiciones = formulario_posiciones()
    return render(request,'rfl-arbitraje.html',{'lva_1':fomulario_subida,'formulario_posiciones':f_posiciones})

def llegada_rfl_1(request):
    if request.method=='POST':
        formularios = lva_1_2(request.POST,request.FILES)
        if formularios.is_valid():
            riskamerica = request.FILES['rsk']
            telerenta = request.FILES['tr']
            f_tr = io.TextIOWrapper(telerenta.file, encoding='utf-8-sig')
            f_rsk = io.TextIOWrapper(riskamerica.file,encoding='utf-8-sig')
            csv_tr = csv.DictReader(f_tr,delimiter=";",dialect='excel')
            csv_rsk = csv.DictReader(f_rsk,delimiter=";",dialect='excel')
            risk.objects.all().delete()
            tr.objects.all().delete()       
            if 'Cantidad' not in csv_tr.fieldnames:
                csv_tr.fieldnames = ["Instrumento","Tipo","N° Negocios","Cantidad","Reaj.","Monto $","Precio Mayor","Precio Menor","Precio Medio","TIR Mayor","TIR Menor","TIR Media","Duration","Precio Cierre","Fecha de Cierre"]
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
                if 'E+' in monto_outstanding:
                    y = re.sub(r"\d*,?\d+E\+\d+","100",monto_outstanding)
                    monto_outstanding = y
                f = risk(nemo=nemo,tipo=tipo,riesgo=riesgo,moneda=moneda,monto_outstanding=monto_outstanding,duracion=duracion,tir=tir)
                f.save()
            f_tr.close()
            f_rsk.close()
            limpia_risk()
            actualiza_riesgo()
            actualiza_tipo()
            return redirect('consulta_cintas')
        else:
            messages.error(request,'El archivo no es correcto,¿tiene formato utf-8 y separado por ; ? ')
            return redirect('arbitraje_rfl')
    
    return HttpResponse("Conectado")

def consulta_cintas(request):
    f_consulta_cintas = formulario_consulta_cintas()
    return render(request,'rfl-arbitraje-consultas.html',{'formulario_consulta_cintas':f_consulta_cintas})


def consulta_cintas_proceso(request):
    datos = {}
    categoria = request.GET.get('categoria')
    rating = request.GET.get('rating')
    moneda = request.GET.get('moneda')
    duracion_inicial = request.GET.get('duracion_inicial')
    duracion_final = request.GET.get('duracion_final')
    texto = "Bonos {} en {} {} duración entre {} y {}".format(categoria,moneda,rating,duracion_inicial,duracion_final)
    datos['titulo'] = texto 
    
    #Falta pensar en alguna forma de rellenar los ratings de riesgo

    print(categoria,rating,moneda,duracion_inicial,duracion_final)
    consulta_tr = tr.objects.filter(tipo=categoria,rating=rating, reajuste=moneda,duracion__range=(duracion_inicial,duracion_final)).values('instrumento','tir_media','duracion','rol_tr')
    consulta_rsk = risk.objects.filter(tipo = categoria,riesgo = rating,moneda = moneda,monto_outstanding__gt=0,duracion__range=(duracion_inicial,duracion_final)).values('nemo','tir','duracion','rol_rsk')
    #acá creamos la consulta que saca de risk los que están en tr
    
    datos['c'] = consulta_tr.union(consulta_rsk, all=True)
    if consulta_rsk.exists() and consulta_tr.exists():
        return render(request,'rfl-arbitraje-consultas-salida.html',context=datos)
    elif consulta_rsk.exists() and consulta_tr.exists()==False:
        texto = texto + '.No hay resultado en Telerrenta.'
        datos['titulo'] = texto
        return render(request,'rfl-arbitraje-consultas-salida.html',context=datos)
    elif consulta_rsk.exists()==False and consulta_tr.exists():
        texto = texto + '. No hay resultado en Riskamérica.'
        datos['titulo'] = texto
        return render(request,'rfl-arbitraje-consultas-salida.html',context=datos)
    else:
        texto = texto + '. No hay resultado ni en Riskamérica ni en Telerrenta.'
        datos['titulo'] = texto
        return render(request,'rfl-arbitraje-consultas-salida.html',context=datos)


# def llegada_posiciones(request):
#     if request.method=='POST':
#         f=formulario_posiciones(request.POST,request.FILES)
#         if f.is_valid():
#             f_tr = io.TextIOWrapper(f.file, encoding='utf-8-sig')


    
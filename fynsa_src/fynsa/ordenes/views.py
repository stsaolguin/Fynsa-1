from django.db import close_old_connections
from django.http.response import HttpResponse
from django.shortcuts import render
from ordenes.formularios_ordenes import rfi_ingreso_orden_formulario
from RFI.models import rfi_bonos
from ordenes.models import rfi_tsox
from django.core import serializers
import ast,time


def rfi_ingreso_ordenes(request):
    
    if request.method=='POST':
        f = rfi_ingreso_orden_formulario(request.POST)
        if f.is_valid():
            #acá procesamos la vista correcta
            precio = request.POST.get('precio')
            precio = precio.replace(',','.')
            nominales = request.POST.get('nominales')
            nominales = nominales.replace('.','')
            e = rfi_tsox()
            e.trader =request.user
            e.fecha_ingreso = request.POST.get('fecha_ingreso')
            e.orden_tipo = request.POST.get('orden_tipo')
            e.isin = request.POST.get('isin')
            e.papel = request.POST.get('papel')
            e.cliente = request.POST.get('cliente')
            e.rating = request.POST.getlist('rating')
            e.pais = request.POST.getlist('pais')
            e.duracion = request.POST.getlist('duracion')
            e.nominales = nominales
            e.sector = request.POST.getlist('sector')
            e.precio = precio
            e.payment_rank = request.POST.getlist('payment_rank')
            e.ytm = request.POST.getlist('ytm')
            e.notas = request.POST.get('notas')
            e.status ='Firme'
            e.save()
            print('datos guardados')
            datos={}
            datos['formulario']=rfi_ingreso_orden_formulario()
            return render(request,'ordenes/rfi-ingreso-ordenes.html',context=datos)

        else:
            datos={}
            datos['formulario']=rfi_ingreso_orden_formulario(request.POST)
            return render(request,'ordenes/rfi-ingreso-ordenes.html',context=datos)
    datos={}
    datos['formulario']=rfi_ingreso_orden_formulario()
    return render(request,'ordenes/rfi-ingreso-ordenes.html',context=datos)


def rfi_prueba_arreglo(request):
    """Esta vista es para probar cómo funcionaría un formulario con array
    hay borrarla mas adelante con la url correspondiente  """
    datos = {}
    datos['formulario']=PruebaArregloForm()
    if request.method=='POST':
        print(request.POST)
        c = PruebaArregloForm(request.POST)
        if c.is_valid():
            c.save()

    return render(request,'prueba-array.html',context=datos)


def security_name_api(request,isin):
    """ Esta función es el endpoint del fecth de  """
    #hagamos el caso donde siempre funcione
    consulta = rfi_bonos.objects.filter(ising=isin)
    consulta_json = serializers.serialize('json',consulta)
    return HttpResponse(consulta_json,content_type='application/json')

def listado_ordenes(request):
    """ Lista las ordenes puestas en pantalla """
    datos = {}
    datos['listado'] = rfi_tsox.objects.all()
    return render(request,'ordenes/rfi-listado-ordenes.html',context=datos)

def actualiza_status(request):
    """ Función para actualizar el estatus a intencion a firme"""
    print(request.POST)
    #rfi_tsox.objects.filter(id=orden_numero).update(status=nuevo_status)
    return True

def busca_papeles(request):
    if request.POST:
        datos = {}
        paises = request.POST.getlist("paises") or None
        sector = request.POST.getlist("sector") or None
        rating = request.POST.getlist("rating") or None
        duracion = request.POST.getlist("duracion") or None
        ytm = request.POST.getlist("ytm") or None
        payment_rank = request.POST.getlist("payment_rank") or None
        pr = [d for d in ast.literal_eval(paises.pop())]
        sr = [e for e in ast.literal_eval(sector.pop())]
        rr = [f for f in ast.literal_eval(rating.pop())]
        dr = [g for g in ast.literal_eval(duracion.pop())]
        yr = [h for h in ast.literal_eval(ytm.pop())]
        pyr = [i for i in ast.literal_eval(payment_rank.pop())]
        resultado = []
        
        comienzo = time.time()
        contador = 0
        conteo_bonos = 0
        for r in rr:
            for s in pr:
                for t in sr:
                    for u in dr:
                        for v in yr:
                            for w in pyr:
                                contador+=1
                                busqueda = rfi_bonos.objects.filter(risk=r,cntry_of_risk=s,industria=t,dur_text=u,yas_bond_text=v,payment_rank=w)
                                if busqueda.exists():
                                    conteo_bonos+=int(len(busqueda))
                                    resultado.append(busqueda)
                                    

        final = time.time()
        tiempo_total = final-comienzo
       
        datos['resultado'] = resultado
        datos['iteraciones'] = contador 
        datos['tiempo'] = tiempo_total
        datos['conteo_bonos'] = conteo_bonos
        return render(request,'ordenes/ordenes-salida-papeles.html',context=datos)
    return HttpResponse("TODO BIEN!")
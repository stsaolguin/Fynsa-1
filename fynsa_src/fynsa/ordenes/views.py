from re import template
from django import forms
from django.db import close_old_connections
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from ordenes.formularios_ordenes import AgregaClientes,IngresoOrdenesRFIModelForm,lista_sector,listado_cntry,FondoOrdenes,BuscadorEditorBonosForm,EditorBonos
from RFI.models import rfi_bonos,clientes_rfi
from ordenes.models import fondo, holders_salida, rfi_tsox, rfi_tsox_borrado,fondo,fondo_salida,carteras_bbg,intenciones_pasadas_salida
from django.core import serializers
import ast,time
from django.urls import reverse_lazy
from itertools import tee
from django.db.models import Q



def rfi_ingreso_ordenes(request):
    
    if request.method=='POST':
        '''Esta vista ya no sirve'''
        print(request.POST)
        f = rfi_ingreso_orden_formulario(request.POST)
        print(f.errors)
        #acá no podemos agregar un cliente nuevo directamente, hay que arreglar
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
    datos['listado'] = rfi_tsox.objects.all().order_by('-fecha_ingreso')
    return render(request,'ordenes/rfi-listado-ordenes.html',context=datos)

def actualiza_status(request,orden_numero,estado):
    """ Función para actualizar el estatus a intencion a firme"""
    rfi_tsox.objects.filter(id=orden_numero).update(status=estado)
    q = rfi_tsox.objects.filter(id=orden_numero)
    actualizacion = serializers.serialize('json',q)
    return HttpResponse(actualizacion,content_type='application/json')

def actualiza_status_fondo(request,orden_numero_fondo,estatus,tipo):
    """ Función para actualizar el estatus de las salida de los matcheos"""
    print(orden_numero_fondo,estatus,tipo)
    if tipo == 'fondo':
        fondo_salida.objects.filter(id=orden_numero_fondo).update(status_asignado = estatus)
        q = fondo_salida.objects.filter(id=orden_numero_fondo)
        actualizacion = serializers.serialize('json',q)
        return HttpResponse(actualizacion,content_type='application/json')
    elif tipo == 'intencion':
        print('pasando por aca')
        intenciones_pasadas_salida.objects.filter(id=orden_numero_fondo).update(status_intencion_asignada = estatus)
        q = intenciones_pasadas_salida.objects.filter(id=orden_numero_fondo)
        actualizacion = serializers.serialize('json',q)
        return HttpResponse(actualizacion,content_type='application/json')
    elif tipo == 'holder':
        holders_salida.objects.filter(id=orden_numero_fondo).update(status_holder_asignada = estatus)
        q = holders_salida.objects.filter(id=orden_numero_fondo)
        actualizacion = serializers.serialize('json',q)
        return HttpResponse(actualizacion,content_type='application/json')
    
        


def actualiza_notas_fondo(request):
    #Dentro de actualiza notas fondo
    if request.POST:
        numero_fondo = request.POST.get('id_fondo')
        notas = request.POST.get('notas_fondo')
        fondo_salida.objects.filter(id=numero_fondo).update(notas_asignado=notas)
        q = fondo_salida.objects.filter(id=numero_fondo)
        salida = serializers.serialize('json',q)
        return HttpResponse(salida,content_type='application/json')
    return HttpResponse('Error')
    
def busca_papeles(request):
    
    if request.POST:
        datos = {}
        paises = request.POST.getlist("paises") or None
        sector = request.POST.getlist("sector") or None
        rating = request.POST.getlist("rating") or None
        duracion = request.POST.getlist("duracion") or None
        ytm = request.POST.getlist("ytm") or None
        payment_rank = request.POST.getlist("payment_rank") or None
        datos['unico_orden'] = unico_orden = request.POST.get("unico_orden")
        datos['cliente'] = request.POST.get("cliente")
        paises2 = str(paises)
        sector2 = str(sector)
        rating2 = str(rating)
        duracion2 = str(duracion)
        ytm2 = str(ytm)
        payment_rank2 = str(payment_rank)
        datos['paises'] = paises2 = paises2.replace('["[\'','').replace('\']"]','')
        datos['sector'] = sector2 = sector2.replace('["[\'','').replace('\']"]','')
        datos['rating'] = rating2 = rating2.replace('["[\'','').replace('\']"]','')
        datos['duracion'] = duracion2 = duracion2.replace('["[\'','').replace('\']"]','')
        datos['ytm'] = ytm2 = ytm2.replace('["[\'','').replace('\']"]','')
        datos['payment_rank'] = payment_rank2 = payment_rank2.replace('["[\'','').replace('\']"]','')
        datos['cliente'] = request.POST.get('cliente')
        datos['trader'] = request.user
        isin = request.POST.get("isin")
        security_name = request.POST.get("security_name")
        #procesado de las listas
        paises_lista = ast.literal_eval(paises[0])
        sector_lista = ast.literal_eval(sector[0])
        rating_lista = ast.literal_eval(rating[0])
        duracion_lista = ast.literal_eval(duracion[0])
        ytm_lista = ast.literal_eval(ytm[0])
        payment_rank_lista = ast.literal_eval(payment_rank[0])
        resultado = []
        comienzo = time.time()
        contador = 0
        conteo_bonos = 0
        if request.POST.get('papeles')=='papeles':
            busqueda = rfi_bonos.objects.filter(
                bb_composite__in = rating_lista,
                cntry_of_risk__in = paises_lista,
                industria__in = sector_lista,
                dur_text__in = duracion_lista,
                yas_bond_text__in = ytm_lista,
                payment_rank__in = payment_rank_lista
                ) 
            if busqueda.exists():
                final = time.time()
                tiempo_total = final-comienzo
                datos['tiempo'] = tiempo_total
                datos['conteo_bonos'] = busqueda.count()
        
            datos['resultado'] = busqueda
            
            return render(request,'ordenes/ordenes-salida-papeles.html',context=datos)

        #acá abajo empieza el proceso de los fondos                                
        elif request.POST.get('fondos')=='fondos':
            s = rfi_tsox.objects.get(pk=unico_orden)
            if not fondo_salida.objects.filter(orden_asignada=unico_orden).exists():
                q = fondo.objects.filter(
                    duracion_fondo__overlap = duracion_lista,
                    sector_fondo__overlap = sector_lista,
                    ytm_fondo__overlap = ytm_lista,
                    risk_fondo__overlap = rating_lista,
                    cntry_of_risk_fondo__overlap  = paises_lista)
                for r in q:                
                    fondo_salida.objects.create(orden_asignada = s,fondo_asignado = r)

            #acá hay que filtrar por holders
            if not holders_salida.objects.filter(orden_asignada = unico_orden).exists():
                #primero traemos los holders que tienen ese isin
                q = carteras_bbg.objects.filter(isin = isin) 
                for r in q:
                    #... y luego los grabamos en el objeto
                    holders_salida.objects.create(orden_asignada = s, holder_asignada = r)
                

                #holders_por_nemo = carteras_bbg.objects.filter(nemo = security_name) 
            
            #acá filtramos en las intenciones
            if not intenciones_pasadas_salida.objects.filter(orden_asignada = unico_orden).exists():
                #traemos las intenciones pasadas que tienen ese isin
                q = rfi_tsox_borrado.objects.filter(Q(isin = isin) | Q(papel__iexact = security_name))
                #traemos las intenciones pasadas que tienen ese security_name
                                
                for r in q:
                    intenciones_pasadas_salida.objects.create(orden_asignada = s, intencion_pasada_asignada = r)
                papeles_intenciones_isin = rfi_tsox_borrado.objects.filter(isin = isin).order_by('-fecha_ingreso')
                #papeles_intenciones_nemo = rfi_tsox_borrado.objects.filter(papel = security_name).order_by('-fecha_ingreso')
                
            datos['resultado'] = q = fondo_salida.objects.filter(orden_asignada=unico_orden).order_by("id")
            datos['holders_por_isin'] = holders_salida.objects.filter(orden_asignada=unico_orden).order_by("id")
            datos['papeles_intenciones_isin'] = intenciones_pasadas_salida.objects.filter(orden_asignada=unico_orden).order_by("id")
            final = time.time()
            tiempo_total = final-comienzo
            datos['iteraciones'] = contador 
            datos['tiempo'] = tiempo_total
            datos['conteo_bonos'] = len(q)
            datos['papel'] = security_name
            datos['isin'] = isin
            return render(request,'ordenes/ordenes-salida-fondos.html',context=datos)
    return HttpResponse("Hay un error!")

def EditarOrden(request,numero):
    """Para que funcione bien esta función hay que cambiar el formulario de ingreso de ordenes a modelform"""
    datos = {}
    orden = rfi_tsox.objects.get(id=numero) #la consulta la convertimos en diccionario
    f = rfi_ingreso_orden_formulario(instance=orden) 
    datos['formulario'] = f #llenamos el formulario
    return render(request,'ordenes/rfi-ingreso-ordenes.html',context=datos)

def BorrarOrden(request,numero):
    """ Pero no está en uso. Esta función tiene por objectivo borrar la orden definitivamente o mandarla a intenciones."""
    q = rfi_tsox.objects.filter(id=numero)
    for r in q.values():
        rfi_tsox_borrado.objects.create(**r)
    q.delete()
    return redirect('listado_ordenes')

class CrearClienteCreateView(CreateView):
    #context_object_name = 'formulario'
    form_class = AgregaClientes
    template_name = "ordenes/ordenes-listar-clientes.html"
    def form_valid(self, form):
        self.object = form
        self.object.save()
        return HttpResponseRedirect('ordenes/ordenes-agregar-exitoso.html')


class rfi_ingreso_ordenes_modelform(SuccessMessageMixin,CreateView):
    model = rfi_tsox
    form_class = IngresoOrdenesRFIModelForm
    template_name = 'ordenes/rfi-ingreso-ordenes-modelform.html'
    success_url = reverse_lazy('rfi_ingreso_ordenes_modelform')
    success_message = "Orden agregada exitosamente"
    def form_valid(self, form):
        o = form.save(commit=False)
        o.trader = str(self.request.user)
        o.save()
        return super().form_valid(form)

class ordenes_updatea_orden(UpdateView):
    model = rfi_tsox
    form_class = IngresoOrdenesRFIModelForm
    template_name = 'ordenes/rfi-ingreso-ordenes-modelform.html'
    success_url = reverse_lazy('listado_ordenes')
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class ordenes_borra_orden(DeleteView):
    model = rfi_tsox
    template_name = 'ordenes/ordenes_borrar_orden_confirmacion.html'
    success_url = reverse_lazy('listado_ordenes')
    def post(self,request,*args,**kwargs):
        if request.POST.get('accion') == 'Intención operado Fynsa':
            q = rfi_tsox.objects.filter(id=kwargs['pk'])
            for r in q.values():
                s = rfi_tsox_borrado.objects.create(**r)
                if not request.POST.get('notas') == '':
                    notas = request.POST.get('notas')
                    s.notas = notas
                    s.status = 'operado Fynsa'
                    s.save()
            return self.delete(request,*args,**kwargs)
        elif request.POST.get('accion') == 'Intención operado Away':
            q = rfi_tsox.objects.filter(id=kwargs['pk'])
            for r in q.values():
                s = rfi_tsox_borrado.objects.create(**r)
                if not request.POST.get('notas') == '':
                    notas = request.POST.get('notas')
                    s.notas = notas
                    s.status = 'operado Away'
                    s.save()
        return self.delete(request,*args,**kwargs)

class ordenes_crea_fondo(CreateView):
    model = fondo
    form_class = FondoOrdenes
    template_name = 'ordenes/ordenes-crea-fondo.html'
    success_url = reverse_lazy('listar_fondo')
    
class ordenes_lista_fondos(ListView):
    model = fondo
    ordering = 'nombre_fondo'
    template_name ='ordenes/ordenes-listado-fondos.html'

class ordenes_updatea_fondo(UpdateView):
    model = fondo
    form_class = FondoOrdenes
    template_name = 'ordenes/ordenes-crea-fondo.html'
    success_url = reverse_lazy('listar_fondo')

class ordenes_borrar_fondo(DeleteView):
    model = fondo
    template_name = 'ordenes/ordenes_borrar_fondo_confirmacion.html'
    success_url = reverse_lazy('listar_fondo')


def salida_fondos(request):
    return render(request,'ordenes/pruebas-ordenes-salida-fondos.html',context={})

from django.db.models.signals import post_save
from django.dispatch import receiver
from ordenes.models import rfi_tsox

@receiver(post_save, sender=rfi_tsox)
def my_handler(sender, **kwargs):
    #esta función estaba probando las signasl de Dajngo. Se puede borrar luego
    j = kwargs['instance']    
    if fondo_salida.objects.filter(orden_asignada=j.id).exists():
        fondo_salida.objects.filter(orden_asignada=j.id).delete()
        q = fondo.objects.filter(duracion_fondo__contains=j.duracion,sector_fondo__contains=j.sector,ytm_fondo__contains=j.ytm,risk_fondo__contains=j.rating,cntry_of_risk_fondo__contains=j.pais)
        s = rfi_tsox.objects.get(pk=j.id)
        for r in q:
            fondo_salida.objects.create(orden_asignada = s,fondo_asignado=r)
               
from BASES.formularios_bases import cargador_bases_form2
def prueba_lectura_carpeta(request):
    f = cargador_bases_form2()
    if request.method =='POST':
        f = cargador_bases_form2(request.POST,request.FILES)
        archivos = request.FILES.getlist('ruta')
        if f.is_valid():
            for archivo in archivos:
                if archivo.name[0]=='V':
                    print(archivo.name)
                    #for r in archivo.readlines():
                        #print(r)
                                
            return HttpResponse(f)
    return render(request,'ordenes/pruebas-lectura-carpeta.html',context={'formulario':f })


def buscador_intenciones(request):
    return render(request,'ordenes/ordenes-buscador-intenciones.html',context={})


def buscador_bonos(request):
    f = BuscadorEditorBonosForm()
    return render(request,'ordenes/ordenes-buscador-bonos.html',context={'formulario':f})

def ordenes_updatea_bono(request):
    if request.method == 'POST' and request.POST.get('botón')=='Editor':
        isin = request.POST.get('isin_security_name')
        f = BuscadorEditorBonosForm(request.POST)
        if f.is_valid():
            q = rfi_bonos.objects.get(ising = isin)
            formulario_bono = EditorBonos(instance=q)
            return render(request,'ordenes/ordenes-crea-edita-bono.html',context={'form':formulario_bono})
    elif request.method == 'POST' and request.POST.get('botón')=='Agregar Bono':
        formulario_bono = EditorBonos()
        return render(request,'ordenes/ordenes-crea-edita-bono.html',context={'form':formulario_bono})

#from django.contrib import messages
def ordenes_graba_bono(request):
    if request.method == 'POST':
        print(request.POST)
        isin = request.POST.get('ising')
        f = EditorBonos(request.POST)
        datos_bono_2 = request.POST.copy()
        datos_bono_2.pop('csrfmiddlewaretoken')
        datos_bono = datos_bono_2.dict() #los querydict dan problemas, hay que pasarlos a diccionario python
        if f.is_valid():
            try:
                obj = rfi_bonos.objects.get(ising=isin)
                for key, value in datos_bono.items():
                    setattr(obj,key,value)
                obj.save()
            except rfi_bonos.DoesNotExist:
                obj = rfi_bonos(**datos_bono)
                obj.save()
    return render(request,'ordenes/ordenes-agregar-exitoso.html',context={})

            


           
    




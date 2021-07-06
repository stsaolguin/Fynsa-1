from re import template
from django import forms
from django.db import close_old_connections
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from ordenes.formularios_ordenes import AgregaClientes,IngresoOrdenesRFIModelForm,lista_sector,listado_cntry,FondoOrdenes
from RFI.models import rfi_bonos,clientes_rfi
from ordenes.models import fondo, rfi_tsox, rfi_tsox_borrado,fondo,fondo_salida
from django.core import serializers
import ast,time
from django.urls import reverse_lazy
from itertools import tee

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
    datos['listado'] = rfi_tsox.objects.all().order_by('id')
    return render(request,'ordenes/rfi-listado-ordenes.html',context=datos)

def actualiza_status(request,orden_numero,estado):
    """ Función para actualizar el estatus a intencion a firme"""
    rfi_tsox.objects.filter(id=orden_numero).update(status=estado)
    q = rfi_tsox.objects.filter(id=orden_numero)
    actualizacion = serializers.serialize('json',q)
    return HttpResponse(actualizacion,content_type='application/json')

def actualiza_status_fondo(request,orden_numero_fondo,estatus):
    """ Función para actualizar el estatus a intencion a firme"""
    fondo_salida.objects.filter(id=orden_numero_fondo).update(status_asignado=estatus)
    q = fondo_salida.objects.filter(id=orden_numero_fondo)
    actualizacion = serializers.serialize('json',q)
    return HttpResponse(actualizacion,content_type='application/json')

def busca_papeles(request):
    
    if request.POST:
        datos = {}
        paises = request.POST.getlist("paises") or None
        sector = request.POST.getlist("sector") or None
        rating = request.POST.getlist("rating") or None
        duracion = request.POST.getlist("duracion") or None
        ytm = request.POST.getlist("ytm") or None
        payment_rank = request.POST.getlist("payment_rank") or None
        unico_orden = request.POST.get("unico_orden")
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
        pr = [d for d in ast.literal_eval(paises.pop())] if not '''['Todos']''' in paises else None
        sr = [e for e in ast.literal_eval(sector.pop())] if not '''['Todos']''' in sector else None
        rr = [f for f in ast.literal_eval(rating.pop())] if not '''['Todos']''' in rating else None
        dr = [g for g in ast.literal_eval(duracion.pop())] if not '''['Toda la curva']''' in duracion else None
        yr = [h for h in ast.literal_eval(ytm.pop())] if not '''['Todos']''' in ytm else None
        pyr = [i for i in ast.literal_eval(payment_rank.pop())] if not '''['Todos']''' in payment_rank else None
        resultado = []
        comienzo = time.time()
        contador = 0
        conteo_bonos = 0
        #if pr is None and rr is None and rr is None and dr is None and yr is None and pyr is None:
        #   busqueda = rfi_bonos.objects.all()
        if request.POST.get('papeles')=='papeles':
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
        #acá abajo empieza el proceso de los fondos                                
        elif request.POST.get('fondos')=='fondos':
            if not fondo_salida.objects.filter(orden_asignada=unico_orden).exists():
                q = fondo.objects.filter(duracion_fondo__contains=dr,sector_fondo__contains=sr,ytm_fondo__contains=yr,risk_fondo__contains=rr,cntry_of_risk_fondo__contains=pr)
                s = rfi_tsox.objects.get(pk=unico_orden)
                for r in q:                
                    fondo_salida.objects.create(orden_asignada = s,fondo_asignado = r)

            datos['resultado'] = q = fondo_salida.objects.filter(orden_asignada=unico_orden)
            final = time.time()
            tiempo_total = final-comienzo
            datos['iteraciones'] = contador 
            datos['tiempo'] = tiempo_total
            datos['conteo_bonos'] = len(q)
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
    """ Esta función tiene por objectivo borrar la orden y copiarla a otra tabla, no la borra totalmente, la saca."""
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


class rfi_ingreso_ordenes_modelform(CreateView):
    model = rfi_tsox
    form_class = IngresoOrdenesRFIModelForm
    template_name = 'ordenes/rfi-ingreso-ordenes-modelform.html'
    success_url = reverse_lazy('rfi_ingreso_ordenes_modelform')
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
        q = rfi_tsox.objects.filter(id=kwargs['pk'])
        for r in q.values():
            s = rfi_tsox_borrado.objects.create(**r)
            if not request.POST.get('notas') == '':
                notas = request.POST.get('notas')
                s.notas = notas
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
    j = kwargs['instance']    
    if fondo_salida.objects.filter(orden_asignada=j.id).exists():
        fondo_salida.objects.filter(orden_asignada=j.id).delete()
        q = fondo.objects.filter(duracion_fondo__contains=j.duracion,sector_fondo__contains=j.sector,ytm_fondo__contains=j.ytm,risk_fondo__contains=j.rating,cntry_of_risk_fondo__contains=j.pais)
        s = rfi_tsox.objects.get(pk=j.id)
        for r in q:
            fondo_salida.objects.create(orden_asignada = s,fondo_asignado=r)
               
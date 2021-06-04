from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.shortcuts import render,redirect
from django.core import serializers
from BASES.models import bases,facturas_bases
from .formularios_bases import *
from RFL.models import actividad
from .funciones_externas_Bases import *
from django.views.generic import ListView
import csv

def comite_bases(request):
    fechas_ingreso=f_fechas_comite()
    form_conciliaciones=f_conciliaciones()
    return render(request,'comite-bases.html',{'fechas_ingreso':fechas_ingreso,'formulario_conciliaciones':form_conciliaciones})

def ingreso_bases(request):
    formulario_ingreso_bases = f_bases()
    return render(request,'ingreso-bases.html',{'formulario_ingreso_bases':formulario_ingreso_bases})
def procesa_ingreso_bases(request):
    if request.method=='POST':
        formulario_ingreso_bases=f_bases(request.POST)
        if formulario_ingreso_bases.is_valid():
            formulario_ingreso_bases.save()
            return redirect('bases')
        return render(request,'ingreso-bases.html',{'formulario_ingreso_bases':formulario_ingreso_bases})         

def salida_bases(request):
    if request.method=='POST':
        
        datos={}
        fechas=request.POST.copy()
        
        fecha_inicial = fechas['fecha_inicial']
        fecha_final = fechas['fecha_final']
        datos['fecha_inicial']=parse_date(fecha_inicial)
        datos['fecha_final']=parse_date(fecha_final)
        
        
        
        #aca comenzamos con las consultas a la db.
        datos['lista_depositos_via_tasa'] = bases.objects.raw(''' select 1 as linea, cliente, util_tasa from eqder_generacion_tasas(%s,%s,'F') where util_tasa<>0 order by util_tasa desc ''',[fecha_inicial,fecha_final])
        datos['lista_bases_via_tasa'] = bases.objects.raw(''' select 1 as linea, cliente, util_tasa from eqder_generacion_tasas(%s,%s,'B') where util_tasa<>0 order by util_tasa desc ''',[fecha_inicial,fecha_final])
        datos['lista_provisiones_por_bases'] = bases.objects.raw(''' select 1 as linea, cliente,round(provision,0) as pro from eqder_generaciones_bases(%s,%s) where provision<>0 order by provision desc; ''',[fecha_inicial,fecha_final])
        datos['lista_provisiones_por_depos'] = bases.objects.raw(''' select 1 as linea, * FROM eqder_provisiones(%s,%s,'F') where provision>0 order by provision desc;''',[fecha_inicial,fecha_final])
        datos['mt_otc_bases'] = bases.objects.raw(''' select 1 as linea, * from eqder_montos_transados(%s,%s,'OTC','B') where monto_transado<>0 order by monto_transado desc ''',[fecha_inicial,fecha_final])
        datos['mt_tr_bases'] = bases.objects.raw(''' select 1 as linea, * from eqder_montos_transados(%s,%s,'TR','B') where monto_transado<>0 order by monto_transado desc ''',[fecha_inicial,fecha_final])
        datos['mt_otc_depos'] = bases.objects.raw(''' select 1 as linea, * from eqder_montos_transados(%s,%s,'OTC','F') where monto_transado<>0 order by monto_transado desc ''',[fecha_inicial,fecha_final])
        datos['mt_tr_depos'] = bases.objects.raw(''' select 1 as linea, * from eqder_montos_transados(%s,%s,'TR','F') where monto_transado<>0 order by monto_transado desc ''',[fecha_inicial,fecha_final])
        datos['torta_generaciones'] = bases.objects.raw(''' select 1 as linea, * from eqder_torta_generaciones(%s,%s)  ''',[fecha_inicial,fecha_final])
        datos['torta_montos_transados'] = bases.objects.raw(''' select 1 as linea, * from eqder_torta_montos_transados(%s,%s)  ''',[fecha_inicial,fecha_final])
        datos['serie_generaciones'] = bases.objects.raw(''' select 1 as linea,fecha,sum(util_depo+fee_buyer_clp+fee_seller_clp) as monto from "BASES_bases" where util_depo>0 or fee_buyer_clp>0 or fee_seller_clp>0 group by fecha HAVING fecha BETWEEN %s and %s order by fecha asc  ''',[fecha_inicial,fecha_final])
        #datos['serie_generaciones_apiladas'] = bases.objects.raw(''' select 1 as linea,fecha,sum(util_depo) as util_depo, sum(fee_buyer_clp+fee_seller_clp) as provision from "BASES_bases" where (util_depo>0 or fee_buyer_clp>0 or fee_seller_clp>0) and fecha BETWEEN %s and %s group by fecha order by fecha asc   ''',[fecha_inicial,fecha_final])
        datos['serie_generaciones_apiladas'] = bases.objects.raw(''' select 1 as linea,* from eqder_serie_generaciones_categorias(%s,%s) order by fecha_salida asc;   ''',[fecha_inicial,fecha_final])
        datos['total_generaciones'] = bases.objects.raw(''' select 1 as linea,COALESCE(sum(util_depo+fee_buyer_clp+fee_seller_clp),0) as monto from "BASES_bases" where (util_depo>0 or fee_buyer_clp>0 or fee_seller_clp>0) and fecha BETWEEN %s and %s  ''',[fecha_inicial,fecha_final])[0]
        datos['total_generaciones_bases'] = bases.objects.raw(''' select 1 as linea, COALESCE(sum(fee_buyer_clp+fee_seller_clp+util_depo),0) as monto_bases from "BASES_bases" where fecha between %s and %s and nemo ilike 'B%%' and (fee_buyer_clp>0 or fee_seller_clp>0 OR util_depo>0)  ''',[fecha_inicial,fecha_final])[0]
        datos['total_generaciones_depos'] = bases.objects.raw(''' select 1 as linea, COALESCE(sum(fee_buyer_clp+fee_seller_clp+util_depo),0) as monto_depos from "BASES_bases" where fecha between %s and %s and nemo ilike 'F%%' and (fee_buyer_clp>0 or fee_seller_clp>0 OR util_depo>0)  ''',[fecha_inicial,fecha_final])[0]
        
        #datos['cobros'] = bases.objects.raw(''' select 1 as linea,cliente,provision,ida_vuelta,(provision-ida_vuelta)as saldo from generaciones_bases_historico() order by provision desc  ''')
        datos['cobros'] = bases.objects.raw(''' Select 1 as linea,* from cobranzas_view_consolidada where provisiones>0; ''')
        datos['saldo_calle'] = bases.objects.raw(''' Select 1 as linea,sum(saldo) as calle from cobranzas_view_consolidada ''')[0]
        datos['vencimientos'] = bases.objects.raw(''' select 1 as linea,fecha,nemo,dias,monto,buy,seller,tasa,(fecha+dias) as fecha_final from "BASES_bases" where (fecha+dias)>now() order by fecha_final asc;''')[:10]
        datos['serie_montos_transados'] = bases.objects.raw(''' select 1 as linea, fecha,
sum(CASE WHEN otc_tr='TR' and nemo ilike 'B%%' then valor_clp ELSE 0 END) as monto_tr_base,
sum(CASE WHEN otc_tr='TR' and nemo ilike 'F%%' then valor_clp ELSE 0 END) as monto_tr_depo,
sum(CASE WHEN otc_tr='OTC' and nemo ilike 'B%%' then valor_clp ELSE 0 END) as monto_otc_base,
sum(CASE WHEN otc_tr='OTC' and nemo ilike 'F%%' then valor_clp ELSE 0 END) as monto_otc_depo 
from "BASES_bases" 
where fecha between %s and %s
group by fecha
order by fecha asc''',[fecha_inicial,fecha_final])
        
        datos['serie_cobranzas'] = bases.objects.raw(''' select 1 as linea,* from serie_cobranzas_view''')
        datos['idayvueltas'] = bases.objects.raw(''' select 1 as linea, * from "BASES_bases" where fecha between %s and %s and (fee_buyer_clp<0 or fee_seller_clp<0) order by fecha desc''',[fecha_inicial,fecha_final])
        datos['idayvueltas_total'] = bases.objects.raw(''' select 1 as linea, sum(fee_buyer_clp+fee_seller_clp)::money as total_idavuelta from "BASES_bases" where fecha between %s and %s and (fee_buyer_clp<0 or fee_seller_clp<0) ''',[fecha_inicial,fecha_final])[0]
        datos['generaciones_consolidadas'] = bases.objects.raw('''with generacion_consolidada as ( select *,round(total/sum(total/100) over(),2) as porcentaje from eq_der_generacion_total_consolidad(%s,%s)) select 1 as linea,*,sum(porcentaje) over (order by porcentaje desc) as porcentaje_acumulado,row_number() OVER (order by total desc) as ranking from generacion_consolidada where total<>0; ''',[fecha_inicial,fecha_final])        
        datos['instrumentos'] = bases.objects.raw('''select 1 as linea,* from eq_der_instrumentos(%s,%s) where generacion<>0 ''',[fecha_inicial,fecha_final])        
        datos['generacion_diaria'] = bases.objects.raw('''select 1 as linea,* from eq_der_serie_generacion_acumulada_diaria_view ''')
        datos['generacion_mensual'] = bases.objects.raw('''select 1 as linea,* from "BASES_serie_generacion_mensual" order by fecha asc ''')
        datos['clientes_unicos_generacion_diaria'] = ["VISION","FYNSA","FM SURA","FM SECURITY","FM SCOTIABANK","FM SCOTIA","FM SANTANDER","FM MONEDA","FM LARRAINVIAL","FM ITAU","FM FYNSA","FM CREDICORP","FM BTG","FM BICE","FM BCI","FM BANCHILE","CDS PRINCIPAL","CDS EUROAMERICA","CDS BICE","CB VECTOR","CB SCOTIABANK","CB MERRIL LYNCH","CB LARRAINVIAL","CB EUROAMERICA","CB CREDICORP","CB CONSORCIO","CB BTG","CB BCI","CB BANCOESTADO","CB BANCHILE","B SECURITY","B SCOTIABANK TRAD","B SCOTIABANK","B SANTANDER TRAD","B SANTANDER BCE","B SANTANDER","B MERRIL LYNCH","B JPM","B ITAU","B INTERNACIONAL","B HSBC","B FALABELLA TRAD","B FALABELLA BCE","B FALABELLA","B ESTADO TRAD","B ESTADO BCE","B ESTADO","B CONSORCIO TRAD","B CONSORCIO BCE","B CONSORCIO","B CHILE TRAD","B CHILE BCE","B CHILE","B BTG","B BICE","B BCI TRAD","B BCI INV","B BCI BCE","B BCI","AFP PLANVITAL","AFP MODELO","AFP HABITAT","AFP CUPRUM","AFP CAPITAL","AFP AFC","ADC VISION","ADC SANTANDER","ADC NEVASA","ADC BCI"]
        # datos['instrumentos_total'] = bases.objects.raw('''select 1 as linea,* from eq_der_instrumentos_total(%s,%s) where gen<>0 ''',[fecha_inicial,fecha_final])        
        datos['instrumentos_bases'] = bases.objects.raw('''select 1 as linea,* from eq_der_instrumentos_bases(%s,%s) where gen<>0 ''',[fecha_inicial,fecha_final])        
        datos['instrumentos_depos'] = bases.objects.raw('''select 1 as linea,* from eq_der_instrumentos_depos(%s,%s) where gen<>0 ''',[fecha_inicial,fecha_final])        
        datos['conteo'] = bases.objects.raw(''' SELECT 1 as linea,* from eq_der_conteo_operaciones(%s,%s)''',[fecha_inicial,fecha_final])        
        #NO OPERARON Y GENERACION 0 HAY QUE REVISAR
        #datos['no_operaron'] = bases.objects.raw(''' SELECT 1 as linea, nombre FROM "BASES_clientes" where factura=false and nombre not in (SELECT nombre FROM eq_der_generacion_total_consolidad(%s,%s) where total<>0) order by nombre asc ''',[fecha_inicial,fecha_final])        
        datos['no_operaron'] = bases.objects.raw(''' SELECT 1 as linea,  nombre FROM eq_der_generacion_total_consolidad(%s,%s) where total<=0 order by nombre asc ''',[fecha_inicial,fecha_final])        
        datos['facturas'] =facturas_bases.objects.filter(fecha_emision__gte=fecha_inicial)
        timbre = actividad(name='BASES',accion='generacion_comite',usuario=request.user)
        timbre.save()
        return render(request,'salida-bases_copy.html',context=datos)

    return render(request,'salida-bases.html',{})



def detalles_cobranzas(request,cliente):
    
    
    datos={}
    datos['cliente_provisiones_buy'] = bases.objects.filter(buy=str(cliente),fee_buyer_clp__gt=0).order_by('fecha')
    datos['cliente_provisiones_seller'] = bases.objects.filter(seller=cliente,fee_seller_clp__gt=0).order_by('fecha')
    datos['cliente_idayvuelta_buyer'] = bases.objects.filter(buy=cliente,fee_buyer_clp__lt=0).order_by('fecha')
    datos['cliente_idayvuelta_seller'] = bases.objects.filter(seller=cliente,fee_seller_clp__lt=0).order_by('fecha')
    datos['cliente_facturas'] = facturas_bases.objects.filter(cliente=cliente).order_by('-fecha_emision')
    #datos['cliente_provisiones_depos'] = bases.objects.raw('''  select 1 as linea, * FROM "BASES_bases" where nemo ilike 'F%%' and (fee_buyer_clp>0 or fee_seller_clp>0) and (buy=%s or seller=%s) order by fecha asc ''',[cliente,cliente])
    datos['cliente_provisiones_depos'] = bases.objects.filter(participante_1=cliente,participante_2=cliente)
    datos['serie_comportamiento'] = bases.objects.raw('''  select 1 as linea, * FROM eqder_serie_provisiones_clientes(%s) ''',[cliente])
    
    return render(request,'detalles-clientes-bases.html',context=datos)


def conciliaciones_views(request):
    cliente=request.GET.get('cliente')
    cliente = cliente + '%'
    fecha_inicial=request.GET.get('fecha_inicial')
    fecha_final=request.GET.get('fecha_final')

    conciliaciones = bases.objects.raw(''' select 1 as linea,fecha,otc_tr,nemo,monto,tipo_de_pago,buy,seller,trader_buy,trader_seller,
sum(
	CASE WHEN buy ilike %s THEN
	fee_buyer_clp
	ELSE
	0
	END
	)as fe_buyer_clp, 
sum(
	CASE WHEN seller ilike %s THEN
	fee_seller_clp
	ELSE
	0
	END)as fe_seller_clp
from "BASES_bases"
where (buy ilike %s or seller ilike %s) AND (fee_seller_clp<>0 or fee_buyer_clp<>0) and fecha between %s and %s
group by fecha,otc_tr,nemo,monto,tipo_de_pago,buy,seller,trader_buy,trader_seller
order by fecha asc;''',[cliente,cliente,cliente,cliente,fecha_inicial,fecha_final])
    
    salida=[]
    response = HttpResponse(content_type='text/csv')
    nombre_archivo = "{0}_entre_el_{1}_y_{2}".format(cliente,fecha_inicial,fecha_final)
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(nombre_archivo)
    writer = csv.writer(response)
    writer.writerow(['fecha','otc_tr','nemo','monto','tipo_de_pago','buy','seller','trader_buy','trader_seller','fee_buyer_clp','fee_seller_clp'])
    for r in conciliaciones:
        salida.append([r.fecha,r.otc_tr,r.nemo,r.monto,r.tipo_de_pago,r.buy,r.seller,r.trader_buy,r.trader_seller,r.fe_buyer_clp,r.fe_seller_clp])
    writer.writerows(salida)

    timbre = actividad(name='BASES',accion='generacion_conciliaciones',usuario=request.user)
    timbre.save()

    return response


def consolidado_csv_views(request):
    fecha_inicial=request.GET.get('fecha_inicial')
    fecha_final=request.GET.get('fecha_final')
    consolidado = bases.objects.raw(''' with generacion_consolidada as ( select *,round(total/sum(total/100) over(),2) as porcentaje
from eq_der_generacion_total_consolidad(%s,%s)
							)
select 1 as linea,*,sum(porcentaje) over (order by porcentaje desc) as porcentaje_acumulado from generacion_consolidada; ''',[fecha_inicial,fecha_final])
    salida=[]
    response = HttpResponse(content_type='text/csv')
    nombre_archivo = "Generacion_total_consolidada_entre_el_{0}_y_{1}".format(fecha_inicial,fecha_final)
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(nombre_archivo)
    writer = csv.writer(response)
    writer.writerow(['nombre','generacion por depositos','generacion por bases','provision por bases','provision por depos','total','porcentaje','porentaje acumulado'])
    for r in consolidado:
        salida.append([r.nombre,r.gen_depo,r.gen_bases,r.prov_bases,r.prov_depos,r.total,r.porcentaje,r.porcentaje_acumulado])
    writer.writerows(salida)
    timbre = actividad(name='BASES',accion='generacion_consolidada',usuario=request.user)
    timbre.save()
    
    return response




def monto_mensual_cliente_views(request):
    producto = request.GET.get('selectorProductoMonto')
    agno = request.GET.get('selectorAgnoMonto')
    montos = bases.objects.raw(''' select 1 as linea,* from eq_bases_montos_transados_mensual_cliente(true,%s,%s) order by cliente asc ''',[agno,producto])
    salida=[]
    response = HttpResponse(content_type='text/csv')
    p = 'BASES' if producto =='b' else 'DEPOSITOS'
    nombre_archivo = "Montos transados año {0} - {1} por cliente".format(agno,p)
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(nombre_archivo)
    writer = csv.writer(response)
    writer.writerow(['cliente','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'])
    for r in montos:
        salida.append([r.cliente,r.enero,r.febrero,r.marzo,r.abril,r.mayo,r.junio,r.julio,r.agosto,r.septiembre,r.octubre,r.noviembre,r.diciembre])
    writer.writerows(salida)
    timbre = actividad(name='BASES',accion='generacion_montos_mensuales',usuario=request.user)
    timbre.save()
    return response

def gen_mensual_cliente_views(request):
    producto = request.GET.get('selectorProductoGen')
    agno = request.GET.get('selectorAgnoGen')
    generacion = bases.objects.raw(''' select 1 as linea,* from eq_bases_generacion_mensual_cliente(true,%s,%s) order by cliente asc ''',[agno,producto])
    salida=[]
    response = HttpResponse(content_type='text/csv')
    p = 'BASES' if producto =='b' else 'DEPOSITOS'
    nombre_archivo = "Generacion Mensual año {0} - {1} por cliente".format(agno,p)
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(nombre_archivo)
    writer = csv.writer(response)
    writer.writerow(['cliente','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'])
    for r in generacion:
        salida.append([r.cliente,r.gen_enero,r.gen_febrero,r.gen_marzo,r.gen_abril,r.gen_mayo,r.gen_junio,r.gen_julio,r.gen_agosto,r.gen_septiembre,r.gen_octubre,r.gen_noviembre,r.gen_diciembre])
    writer.writerows(salida)
    timbre = actividad(name='BASES',accion='generacion_generaciones_mensuales',usuario=request.user)
    timbre.save()
    return response


def salida_bases_institucion_trader(request):
    fecha_inicial=request.GET.get('fecha_inicial')
    fecha_final=request.GET.get('fecha_final')
    datos={}
    datos['fecha_inicial'] = fecha_inicial
    datos['fecha_final'] = fecha_final
    datos['bases_prov'] = bases.objects.raw(''' SELECT 1 as linea, * FROM eqder_provisiones_trader(%s,%s,'B') where provision<>0 order by provision desc; ''',[fecha_inicial,fecha_final])
    datos['depo_prov'] = bases.objects.raw(''' SELECT 1 as linea, * FROM eqder_provisiones_trader(%s,%s,'F') where provision<>0 order by provision desc; ''',[fecha_inicial,fecha_final])
    datos['base_tasa'] = bases.objects.raw(''' SELECT 1 as linea, * FROM eqder_generacion_tasas_trader(%s,%s,'B') where util_tasa<>0 order by util_tasa desc; ''',[fecha_inicial,fecha_final])
    datos['depo_tasa'] = bases.objects.raw(''' SELECT 1 as linea, * FROM eqder_generacion_tasas_trader(%s,%s,'F') where util_tasa<>0 order by util_tasa desc; ''',[fecha_inicial,fecha_final])
    timbre = actividad(name='BASES',accion='generacion_institucion_trader',usuario=request.user)
    timbre.save()
    return render(request,'salida-bases-institucion-trader.html',context=datos)         
    
def cargador_bases(request):
    if request.method=='POST':
        formulario = cargador_bases_form(request.POST,request.FILES)
        if formulario.is_valid():
            try:
                datos_crudos = request.FILES['bases']
                datos_crudos_salida = io.TextIOWrapper(datos_crudos.file,encoding='utf-8-sig')
                c = limpiador_bases_interno(datos_crudos_salida)
                for r in c:
                        fila = bases(**r)
                        fila.save()
            except ValueError as err:
                datos_error = {}
                datos_error['error'] = err
                return render(request,'errores.html',context=datos_error)
            return redirect('ingreso_bases')
       

    datos = {}
    datos['bf'] = cargador_bases_form()
    return render(request,'cargador-bases.html',context=datos)


def ingreso_operaciones_views(request):
    datos = {}    
    datos['ingreso_operaciones'] = bases_ingreso_operaciones()
    datos['ingreso_operaciones_depositos'] = bases_ingreso_operaciones_depos()
    a = bases.objects.raw(''' select 1 as linea, fecha, sum(fee_buyer_clp+fee_seller_clp) as prov from "BASES_bases" group by fecha order by fecha desc limit 1; ''') 
    for i in a:
        datos['provision'] = i.prov
        fecha_1 = i.fecha 
        break
    b = bases.objects.raw(''' select 1 as linea, fecha, sum(util_depo) as util from "BASES_bases" group by fecha order by fecha desc limit 1; ''')      
    for j in b:
        datos['tasa'] = j.util
        fecha_2=j.fecha
    datos['fecha'] = fecha_2 if fecha_2 >= fecha_1 else fecha_1

    return render(request,'bases-ingreso-operaciones.html',context=datos)

def formulario_bases(request):    
    if request.method=='POST':
        
        datos = request.POST.copy()
        datos['monto'] = datos['monto'].replace('.','')
        datos['venta_depo'] = datos['venta_depo'].replace('.','')
        datos['compra_depo'] = datos['compra_depo'].replace('.','')
        datos['fee_seller_clp'] = datos['fee_seller_clp'].replace('.','')
        datos['fee_buyer_clp'] = datos['fee_buyer_clp'].replace('.','')
        datos['tasa_buyer'] = datos['tasa_buyer'].replace(',','.')
        datos['tasa_seller'] = datos['tasa_seller'].replace(',','.')
        if 'boton_bases' in request.POST:            
            f = bases_ingreso_operaciones(data=datos)
            if f.is_valid():
                para_grabar = f.save(commit=False)
                para_grabar.save(using='pruebas')
                return render(request,'bases-salida-tickets.html',context=datos.dict())
            else:
                diccionario_inicial = {}
                diccionario_inicial['ingreso_operaciones'] =f
                diccionario_inicial['ingreso_operaciones_depositos'] = bases_ingreso_operaciones_depos()
                return render(request,'bases-ingreso-operaciones.html',context=diccionario_inicial)
        elif 'boton_depositos' in request.POST:
            f = bases_ingreso_operaciones_depos(data=datos)
            if f.is_valid():
                para_grabar = f.save(commit=False)
                para_grabar.save(using='pruebas')
                return render(request,'bases-salida-tickets.html',context=datos.dict())
            else:
                diccionario_inicial = {}
                diccionario_inicial['ingreso_operaciones'] = bases_ingreso_operaciones()
                diccionario_inicial['ingreso_operaciones_depositos'] = f
                return render(request,'bases-ingreso-operaciones.html',context=diccionario_inicial)
    return render(request,'bases-ingreso-operaciones.html',context=datos)


def ListTodoBlotterBases(request):
    datos={}
    datos['todo_blotter']=bases.objects.all().order_by('-fecha')[:10]
    return render(request,'listar-blotter.html',context=datos)

def EliminarFilaBlotter(request,linea):
    bases.objects.delete(linea=linea)
    return redirect('listar_blotter')

    
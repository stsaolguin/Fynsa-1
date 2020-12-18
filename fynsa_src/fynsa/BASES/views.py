from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.shortcuts import render,redirect
from django.core import serializers

from BASES.models import bases,facturas_bases
from .formularios_bases import *
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
            print('Formulario Válido')
            return redirect('bases')
        print('Formulario NO válido')
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
        datos['total_generaciones'] = bases.objects.raw(''' select 1 as linea,sum(util_depo+fee_buyer_clp+fee_seller_clp) as monto from "BASES_bases" where (util_depo>0 or fee_buyer_clp>0 or fee_seller_clp>0) and fecha BETWEEN %s and %s  ''',[fecha_inicial,fecha_final])[0]
        datos['total_generaciones_bases'] = bases.objects.raw(''' select 1 as linea, sum(fee_buyer_clp+fee_seller_clp+util_depo) as monto_bases from "BASES_bases" where fecha between %s and %s and nemo ilike 'B%%' and (fee_buyer_clp>0 or fee_seller_clp>0 OR util_depo>0)  ''',[fecha_inicial,fecha_final])[0]
        datos['total_generaciones_depos'] = bases.objects.raw(''' select 1 as linea, sum(fee_buyer_clp+fee_seller_clp+util_depo) as monto_depos from "BASES_bases" where fecha between %s and %s and nemo ilike 'F%%' and (fee_buyer_clp>0 or fee_seller_clp>0 OR util_depo>0)  ''',[fecha_inicial,fecha_final])[0]
        
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
        datos['no_operaron'] = bases.objects.raw(''' SELECT 1 as linea, nombre FROM "BASES_clientes" where factura=false and nombre not in (SELECT nombre FROM eq_der_generacion_total_consolidad(%s,%s) where total<>0) order by nombre asc ''',[fecha_inicial,fecha_final])        
        datos['facturas'] =facturas_bases.objects.filter(fecha_emision__gte=fecha_inicial)

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
    
    return response

def ingreso_operaciones_views(request):
    #esta es cotota
    return render(request,'bases-ingreso-operaciones.html',context={})

def monto_mensual_cliente(request,selectorProductoMonto,selectorAgnoMonto):
    print('selectorProductoMonto,selectorAgnoMonto',selectorProductoMonto,selectorAgnoMonto)
    return HttpResponse("pasé")

def gen_mensual_cliente(request,selectorProductoGen,selectorAgnoGen):
    print('selectorProductoGen,selectorAgnoGen',selectorProductoGen,selectorAgnoGen)
    return HttpResponse("pasé")


from django.shortcuts import render
from RFI.models import rfi_beta
from RFI.models import rfi_generacion_comite_temporal as comite

from BASES.formularios_bases import f_fechas_comite_rfi
from django.utils.dateparse import parse_date
    

def rfi_cruce(request,f):
    fondo = sw.objects.raw(''' select 1 as id, * from dinamico(%s) where dif<>0 order by dif desc; ''',[f])
    ventas = sw.objects.raw(''' select 1 as id, sum(dif) as v from dinamico(%s) where dif<0; ''',[f])
    compras = sw.objects.raw(''' select 1 as id, sum(dif) as s from dinamico(%s) where dif>0; ''',[f])
    dur = sw.objects.raw(''' select 1 as id, * from dinamico_dur(%s); ''',[f])
    paises_hoy = sw.objects.raw(''' select 1 as id,cntry_of_risk,sum(valor_nominal) as vn from "RFI_sw" where cntry_of_risk in ('PE','AR','CO','PA','BR','MX','CL')
and fecha_subida='2019-12-01' and institucion=%s group by cntry_of_risk; ''',[f])
    paises_antes = sw.objects.raw(''' select 1 as id,cntry_of_risk,sum(valor_nominal) as vn from "RFI_sw" where cntry_of_risk in ('PE','AR','CO','PA','BR','MX','CL')
and fecha_subida='2020-01-01' and institucion=%s group by cntry_of_risk; ''',[f])
    sectores_hoy = sw.objects.raw(''' select 1 as id,sector,sum(valor_nominal) as vn from "RFI_sw" where fecha_subida='2019-12-01' and institucion=%s group by sector; ''',[f])
    sectores_antes = sw.objects.raw(''' select 1 as id,sector,sum(valor_nominal) as vn from "RFI_sw" where fecha_subida='2020-01-01' and institucion=%s group by sector; ''',[f])

    if compras[0] is None:
        compras[0]==0
    if ventas[0] is None:
        ventas[0]==0
    
    print('ventas',ventas)
    return render(request,'rfi-cruce.html',{'fondo':fondo,'duracion':dur,'paises_hoy':paises_hoy,'paises_antes':paises_antes,'sectores_hoy':sectores_hoy,'sectores_antes':sectores_antes,'ventas':ventas[0],'compras':compras[0]})
def rfi_comite(request):
    fechas_ingreso=f_fechas_comite_rfi()
    return render(request,'comite-rfi.html',{'fechas_ingreso':fechas_ingreso})

def rfi_comite_proceso(request):
    datos={}
    suma_finales = 0
    suma_brokers = 0
    suma_banco_brokers = 0
    #generacion_total = 0
    fechas = request.GET.copy()
    fecha_inicial = parse_date(fechas['fecha_inicial'])
    fecha_final = parse_date(fechas['fecha_final'])
    datos['fecha_inicial'] = fecha_inicial
    datos['fecha_final'] = fecha_final

    c = rfi_beta.objects.raw('''DELETE FROM "RFI_rfi_generacion_comite_temporal";INSERT INTO "RFI_rfi_generacion_comite_temporal"(pais, categoria, nombre_cliente, generacion_brk, generacion_finales, generacion_bancos_brk, generacion_total, spread_brk, spread_finales, spread_banco_brk, generacion_brk_t_1, generacion_finales_t_1, generacion_bancos_brk_t_1, generacion_total_t_1)
SELECT * from eq_rfi_generacion(%s,%s) WHERE generacion_total<>0;SELECT 1 as linea, * FROM "RFI_rfi_generacion_comite_temporal" order by generacion_total desc; ''',[fecha_inicial,fecha_final])
    datos['rfi_generaciones'] = c
    for r in c:
        suma_finales += r.generacion_finales
        suma_brokers += r.generacion_brk 
        suma_banco_brokers += r.generacion_bancos_brk
        
    
    datos['generacion_finales'] = suma_finales
    datos['generacion_brokers'] = suma_brokers
    datos['generacion_bancos_brokers'] = suma_banco_brokers
    
    generacion_total = rfi_beta.objects.raw('''select 1 as linea, sum(ingreso_mesa) as total from "RFI_rfi_beta" where fecha between %s and %s ''',[fecha_inicial,fecha_final])
    
    for z in generacion_total:
        datos['generacion_total'] = z.total
    datos['cntry_of_risk'] = rfi_beta.objects.raw(''' select 1 as linea,country_of_risk as pais, count(papel) as conteo,sum(ingreso_mesa) as generacion from "RFI_rfi_beta" where fecha between %s and %s group by 2 order by generacion desc''',[fecha_inicial,fecha_final])
    datos['series'] = rfi_beta.objects.raw(''' select 1 as linea, fecha, round(avg(spread_mesa),2) as spread, sum(abs(nominales)) as nominales, sum(ingreso_mesa) as generacion  from "RFI_rfi_beta" where fecha between %s and %s group by fecha order by fecha desc ''',[fecha_inicial,fecha_final])
    datos['generacion_categoria'] = rfi_beta.objects.raw(''' select 1 as linea,categoria,count(categoria) as conteo,sum(generacion_total) as generacion from "RFI_rfi_generacion_comite_temporal" where generacion_total<>0 group by categoria ''',[fecha_inicial,fecha_final])
    datos['generacion_pais'] = rfi_beta.objects.raw(''' select 1 as linea,pais,count(pais) as conteo,sum(generacion_total) as generacion from "RFI_rfi_generacion_comite_temporal" where generacion_total<>0 group by pais ''',[fecha_inicial,fecha_final])
    
    datos['actividad_brokers'] = rfi_beta.objects.raw(''' select 1 as linea, * from eq_rfi_actividad_brokers(%s,%s) where monto<>0 order by monto desc ''',[fecha_inicial,fecha_final])
    #papeles
    datos['papeles'] = rfi_beta.objects.raw(''' select 1 as linea,papel,sum(ingreso_mesa) as ingreso_mesa,count(papel) as conteo,round(avg(spread_mesa),2) as spread_mesa_promedio,sum(abs(nominales)) as nominales from "RFI_rfi_beta" where fecha between %s and %s group by papel order by ingreso_mesa desc ''',[fecha_inicial,fecha_final])
    #abajo se llama la funcion con el crosstab tipo json desde postgresql
    cross = rfi_beta.objects.raw(''' select 1 as linea, * from eq_rfi_generacion_crosstab_3() ''')  
    #acá le damos algo de formato
    datos['operaciones_entre_brks'] = rfi_beta.objects.raw('''select 1 as linea,a.fecha,a.papel,a.comprador,a.vendedor,a.spread_mesa,a.ingreso_mesa,b.categoria,c.categoria from "RFI_rfi_beta" a 
JOIN "RFI_clientes_rfi" b ON a.comprador=b.fondo
JOIN "RFI_clientes_rfi" c ON a.vendedor=c.fondo
where fecha between %s and %s and (
	(b.categoria='DLR' and c.categoria='BKR')
or (b.categoria='BKR' and c.categoria='DLR')
or (b.categoria='BKR' and c.categoria='BKR')
or (b.categoria='DLR' and c.categoria='DLR')
); ''',[fecha_inicial,fecha_final])
    encabezados_query = comite.objects.distinct('pais').values_list('pais',flat=True)
    for r in cross:
        resultado = r.datos 
    tabla = []
    
    
    encabezados = [x for x in encabezados_query]
    encabezados.insert(0,'CATEGORIA')
    tabla.append(encabezados)
    for h in resultado:
        fila=[]
        fila = [v for k,v in h.items()]
        for i,item in enumerate(fila):
            
            if fila[i] is None:
               
               fila[i]=0

        tabla.append(fila)
    
    datos['cross'] = tabla
    datos['metas']=rfi_beta.objects.raw(''' select 1 as linea, date_trunc('month',fecha)::date as mensual,sum(ingreso_mesa) as monto from "RFI_rfi_beta" group by mensual order by mensual asc; ''')
    datos['generacion_mensual'] = rfi_beta.objects.raw('''select 1 as linea,* FROM crosstab('select date_part(''month'',fecha) as mes,date_part(''YEAR'',fecha) as agno,sum(ingreso_mesa)
from "RFI_rfi_beta"
group by mes,agno
order by mes,agno','select m from generate_series(2014,2022) m')
as ct(mes numeric, "2014" numeric, "2015" numeric,"2016" numeric,"2017" numeric,"2018" numeric,"2019" numeric,
	  "2020" numeric,"2021" numeric,"2022" numeric) ''')
    return render(request,'comite-rfi-salida.html',datos)
    
def rfi_comite_cliente(request,cliente):
    datos={}
    
    datos['cliente'] = cliente

    return render(request,'comite-rfi-salida-cliente.html',datos)


## Este archivo prepara la RFI pa subirla
#from funcion_truncar import truncar
import csv

def truncar(numero,decimales):
    
    
    if ',' in numero:
        
        numero_aux=numero.split(',')
        lado_derecho=numero_aux[1]
        lado_izquierdo=numero_aux[0]
        if decimales==0:
            return lado_izquierdo
        if len(lado_derecho)>=decimales:
            lado_derecho=lado_derecho[:decimales]
            numero_final=lado_izquierdo+'.'+lado_derecho
        else:
            numero_final=lado_izquierdo+'.'+lado_derecho
        return numero_final

    elif '.' in numero:
        
        numero_aux=numero.split('.')
        lado_derecho=numero_aux[1]
        lado_izquierdo=numero_aux[0]
        if decimales==0:
            return lado_izquierdo

        if len(lado_derecho)>=decimales:
            lado_derecho=lado_derecho[:decimales]
            numero_final=lado_izquierdo+'.'+lado_derecho
        else:
            numero_final=lado_izquierdo+'.'+lado_derecho

        return numero_final
    else:
        numero_final=numero
        return numero_final
#print(truncar(numero=numero_test,decimales=3))



archivo_entrada = open('/home/gvera/Descargas/nuevo_RFI.csv',mode='r',encoding='utf-8',newline='')
csv_entrada =csv.DictReader(archivo_entrada, delimiter=';')

archivo_salida = open('/home/gvera/Descargas/nuevo_RFI-salida.csv',mode='w',encoding='utf-8',newline='')  
encabezados_salida = ['fecha', 'ejecutivo', 'papel', 'cusip', 'operacion', 'nominales', 'mesa', 'ejecutivo_precio', 'cliente_precio', 'ingreso_ejecutivo', 'ingreso_mesa', 'contraparte', 'spread_mesa', 'comprador', 'vendedor', 'country_of_risk', 'crncy']

csv_salida =csv.DictWriter(archivo_salida, delimiter=';',fieldnames=encabezados_salida)
csv_salida.writeheader()



import re 
for s in csv_entrada:
    
    if s['country_of_risk']=='#N/A Invalid Security' or s['country_of_risk']=='#N/A Field Not Applicable' or s['country_of_risk']=='vencido' or s['country_of_risk']=='called' or s['country_of_risk']=='#N/D':
       s['country_of_risk']='-'
  
    if s['crncy']=='#N/D' or s['crncy']=='#N/A Invalid Security':
        s['crncy']='0'
    
    if s['spread_mesa']=='':
        s['spread_mesa']='0'
    if s['mesa']=='':
        s['mesa']='0'
    if s['ejecutivo_precio']=='':
        s['ejecutivo_precio']='0'
    if s['cliente_precio']=='':
        s['cliente_precio']='0'
    if s['ingreso_ejecutivo']==''or s['ingreso_ejecutivo']==' -   ':
        s['ingreso_ejecutivo']='0'
    if s['ingreso_mesa']=='':
        s['ingreso_mesa']='0'
    
    nom=s['nominales']
    s['nominales']=truncar(numero=nom,decimales=0)
    mesa=s['mesa']
    s['mesa']=truncar(numero=mesa,decimales=3)

    ejecutivo_precio=s['ejecutivo_precio']
    ejecutivo_precio=ejecutivo_precio.replace(',','.')
    s['ejecutivo_precio']=ejecutivo_precio


    cliente_precio=s['cliente_precio']
    cliente_precio=cliente_precio.replace(',','.')
    s['cliente_precio']=cliente_precio
    
    ingreso_ejecutivo=s['ingreso_ejecutivo']
    ingreso_ejecutivo=ingreso_ejecutivo.replace(',','.')
    s['ingreso_ejecutivo']=ingreso_ejecutivo

    ingreso_mesa_1=s['ingreso_mesa']
    ingreso_mesa=truncar(numero=ingreso_mesa_1,decimales=3)
    s['ingreso_mesa']=ingreso_mesa

    spread_mesa = s['spread_mesa']
    spread_mesa = spread_mesa.replace(',','.')
    spread_mesa = truncar(numero=spread_mesa,decimales=3)
    s['spread_mesa']=spread_mesa
    

    csv_salida.writerow(s)

archivo_salida.close()
archivo_entrada.close()



import csv
import re
import pdb

fecha_subida=input('Cuál es la fecha de subida para esta cartera? (dd-mm-aaaa)  :')
archivo_entrada = open('/home/gvera/Descargas/SW_Enero_2020.csv',mode='r',encoding='utf-8',newline='')
csv_entrada =csv.DictReader(archivo_entrada, delimiter=';')
archivo_salida = open('/home/gvera/Descargas/SW_Enero_2020_salida.csv',mode='w',encoding='utf-8',newline='')  
encabezados = csv_entrada.fieldnames
encabezados.append('fecha_subida')
csv_salida =csv.DictWriter(archivo_salida, delimiter=';',fieldnames=encabezados)
csv_salida.writeheader()
for s in csv_entrada:
    if s['cntry_of_risk']=='#N/A Invalid Security' or s['cntry_of_risk']=='#N/A Field Not Applicable' or s['cntry_of_risk']=='vencido' or s['cntry_of_risk']=='called':
       s['cntry_of_risk']='-'
    if s['security_name']=='#N/A Invalid Security':
        s['security_name']='-'

    if s['maturity']=='#N/A Invalid Security' or s['maturity']=='#N/A Field Not Applicable' or s['maturity']=='':
        s['maturity']='-'
    #pdb.set_trace()

    tasa_tir=s['tir_de_compra']
    tasa_tir_num=tasa_tir.replace(',','.')

    if tasa_tir_num.isnumeric():
        if float(tasa_tir_num)>=100.00:
            s['tir_de_compra']='-'
        else:
            s['tir_de_compra']=tasa_tir_num
    else:
        s['tir_de_compra']='-'        

    if re.search('%',str(s['tir_de_compra'])) or s['tir_de_compra']=='':
        s['tir_de_compra']='-'
    if s['tipo_instrumento']=='':
        s['tipo_instrumento']='-'
    

    if s['dur_mid_semi_ann']=='#N/A N/A' or s['dur_mid_semi_ann']=='#N/A Invalid Security':
        s['dur_mid_semi_ann']='-'
    if s['valor_nominal']==' -   ' or s['valor_nominal']=='  -':
        s['valor_nominal']='-' 
    s['fecha_subida']=fecha_subida
    
    valor_nominal=s['valor_nominal']
    if ',' in valor_nominal:
        valor_nominal=valor_nominal.split(',')
        s['valor_nominal']=valor_nominal[0]
    
    dur_mid=s['dur_mid_semi_ann']
    
    dur_mid=dur_mid.replace(',','.')
    mayor_a_tres=False
    if '.' in dur_mid:
        dur_mid_aux=dur_mid.split('.')
        if len(dur_mid_aux[0])>=3:
            mayor_a_tres=True 
        dur_mid_decimals=dur_mid_aux[1]
        if len(dur_mid_decimals)>=2:
            dur_mid=dur_mid_aux[0]+'.'+dur_mid_decimals[:2]
            s['dur_mid_semi_ann']=dur_mid
        else:
            s['dur_mid_semi_ann']=dur_mid

    if mayor_a_tres:
        s['dur_mid_semi_ann']='-'
        
    csv_salida.writerow(s)


archivo_salida.close()
archivo_entrada.close()

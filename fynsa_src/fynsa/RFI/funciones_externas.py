import datetime
import re
from io import StringIO

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

import csv
def limpia_rfi(datos_rfi):
    texto = datos_rfi.read()
    texto = texto.replace('.','').replace(',','.')
    texto = re.sub(';\s+;',';;',texto)
    texto = re.sub(';\s+',';',texto)
    texto = re.sub('\s+;',';',texto)
    texto = texto.replace(')','').replace('(','-')
    texto_listo = StringIO(texto)
    encabezados_salida = [
        "fecha",
        "ejecutivo",
        "cliente",
        "papel",
        "cusip",
        "operacion",
        "nominales",
        "mesa",
        "ejecutivo_precio",
    "cliente_precio", 
    "ingreso_ejecutivo",
    "ingreso_mesa",
    "contraparte",
    "spread_mesa",
    "comprador",
    "vendedor",
    "country_of_risk",
    "crncy",
    "duration",
    "tipo_de_cambio",
    "fecha_subido",
    ]
    csv_entrada = csv.reader(texto_listo,delimiter = ';')
    next(csv_entrada)
    lista = []
    for r in csv_entrada:
        f = datetime.datetime.strptime(r[0],'%d-%m-%Y')
        f2 = datetime.date.strftime(f,'%Y-%m-%d')
        c = dict(zip(encabezados_salida,[f2,r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[18],r[23],r[24]]))
        lista.append(c)
    return lista


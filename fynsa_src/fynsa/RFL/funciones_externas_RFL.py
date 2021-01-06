import settings
import csv
import psycopg2 as ps
from psycopg2 import sql
import os

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



    

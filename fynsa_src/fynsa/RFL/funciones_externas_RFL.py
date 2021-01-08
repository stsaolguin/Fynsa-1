from RFL.models import tr,risk,bonos
from django.db.models import OuterRef,Subquery


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

def actualiza_riesgo():
    for h in tr.objects.all():
        tr.objects.update(riesgo=bonos.objects.get(instrumento=h.instrumento).rating)
    return True or False

    


    

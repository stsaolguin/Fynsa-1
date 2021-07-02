from django import template
import locale
from ordenes.formularios_ordenes  import l_sector,l_paymentRank,l_cntry,l_rating,l_duracion,l_ytm

locale.setlocale(locale.LC_ALL,'')
locale._override_localeconv = {'int_frac_digits':0,'frac_digits': 0}
register = template.Library()

@register.filter(name='tiene_grupo')
def tiene_grupo(user,group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='sep')
def separador_miles(valor):
    return locale.currency(int(valor),grouping=True)

#arreglar este filtro

@register.filter(name='tiene_todos')
def TieneTodos(lis,texto='Todos'):
    if lis==l_sector or lis==l_paymentRank or lis==l_cntry or lis==l_rating or lis==l_duracion or lis==l_ytm:
        return True
    else:
        return False
    

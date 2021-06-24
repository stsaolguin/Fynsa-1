from django import template
import locale
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
    for val in lis:
        if val==texto:
            return True
        else:
            return False



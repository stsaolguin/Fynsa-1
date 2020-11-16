from django import template


register = template.Library()
@register.filter(name='tiene_grupo')
def tiene_grupo(user,group_name):
    return user.groups.filter(name=group_name).exists()
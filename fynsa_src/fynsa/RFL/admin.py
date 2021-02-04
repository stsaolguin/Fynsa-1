from django.contrib import admin
from RFL.models import actividad

class rflactividad(admin.ModelAdmin):
    list_display = ['fecha','name','accion','usuario']

admin.site.register(actividad,rflactividad)



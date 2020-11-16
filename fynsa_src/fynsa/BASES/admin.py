from django.contrib import admin
from BASES.models import facturas_bases,bases,clientes
from .formularios_bases import f_facturas_bases

class FacturasBasesAdmin(admin.ModelAdmin):
    form = f_facturas_bases

class BlotterBasesAdmin(admin.ModelAdmin):
    list_filter = ['fecha']
    list_display = ['fecha','otc_tr','nemo','monto','tipo_de_pago','buy','seller']
    search_fields=['fecha']

class ClientesBasesAdmin(admin.ModelAdmin):
    list_display = ['nombre']

    

admin.site.register(facturas_bases, FacturasBasesAdmin)
admin.site.register(bases, BlotterBasesAdmin)
admin.site.register(clientes, ClientesBasesAdmin)



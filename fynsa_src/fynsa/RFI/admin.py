from django.contrib import admin
from RFI.models import clientes_rfi,rfi_bonos


# Register your models here
class clientesAdmin(admin.ModelAdmin):
    list_display = ('fondo','categoria','pais','final')

class bonosAdmin(admin.ModelAdmin):
    list_display = ('ising','security_name')

admin.site.register(clientes_rfi, clientesAdmin)
admin.site.register(rfi_bonos, bonosAdmin)



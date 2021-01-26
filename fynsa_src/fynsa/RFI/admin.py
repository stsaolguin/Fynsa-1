from django.contrib import admin
from RFI.models import clientes_rfi

# Register your models here
class clientesAdmin(admin.ModelAdmin):
    list_display = ('fondo','categoria','pais','final')

admin.site.register(clientes_rfi, clientesAdmin)



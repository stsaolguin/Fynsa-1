from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('comite/', views.comite_bases, name='bases'),
    path('comite/ingreso-data', views.ingreso_bases, name='ingreso_bases'),
    path('comite/procesa-data', views.procesa_ingreso_bases, name='procesa_ingreso_bases'),
    path('comite/salida', views.salida_bases, name='salida_bases'),
    path('comite/salida/institucion-trader', views.salida_bases_institucion_trader, name='salida_bases_institucion_trader'),
    path('comite/salida/detalles-clientes/<str:cliente>', views.detalles_cobranzas, name='detalles_cobranzas'),
    path('comite/salida/montos-mensual-clientes/', views.monto_mensual_cliente_views, name='monto_mensual_cliente'),
    path('comite/salida/generacion-mensual-clientes/', views.gen_mensual_cliente_views, name='gen_mensual_cliente'),
    path('comite/salida/conciliaciones-csv', views.conciliaciones_views, name='conciliaciones_csv'),
    path('comite/salida/consolidado-csv', views.consolidado_csv_views, name='consolidado_csv'),
    path('bases-ingreso-operaciones', views.ingreso_operaciones_views, name='ingreso_operaciones'),
    ]


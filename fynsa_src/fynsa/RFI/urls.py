from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('cruces/', views.rfi_fondos, name='rfi_cruce'),
    # path('cruces/<str:f>', views.rfi_cruce, name='rfi_cruce_detalles'),
    path('comite-rfi/', views.rfi_comite, name='rfi_comite'),
    path('comite-rfi/proceso', views.rfi_comite_proceso, name='rfi_comite_proceso'),
    path('comite-rfi/proceso/<str:cliente>', views.rfi_comite_cliente),
    path('cargador-ordenes-rfi', views.rfi_cargador_datos, name='rfi_cargador_datos'),
    
    ]
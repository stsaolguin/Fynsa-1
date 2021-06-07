from django.urls import path
from . import views

urlpatterns = [
    path('ingreso-ordenes-rfi', views.rfi_ingreso_ordenes, name='rfi_ingreso_ordenes'),
    path('ingreso-ordenes-rfi-arreglo', views.rfi_prueba_arreglo, name='#'),
    path('api/v1/<str:isin>', views.security_name_api, name='api_security_name'),
    ]
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('comite/', views.comite_rfl, name='rfl'),
    path('arbitraje/', views.arbitraje_rfl, name='arbitraje_rfl'),
    path('arbitraje/llegada', views.llegada_rfl_1, name='llegada_rfl_1'),
    path('arbitraje/llegada-posiciones', views.llegada_posiciones, name='llegada_posiciones'),
    path('arbitraje/llegada-lva', views.llegada_lva, name='llegada_lva'),
    path('arbitraje/cintas', views.consulta_cintas, name='consulta_cintas'),
    path('arbitraje/cintas/consulta', views.consulta_cintas_proceso, name='consulta_cintas_proceso'),
    path('arbitraje/cintas/consulta/<str:bono>', views.consulta_cintas_proceso_grafico, name='consulta_cintas_proceso_grafico'),
    ]

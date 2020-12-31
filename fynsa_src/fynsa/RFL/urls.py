from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('comite/', views.comite_rfl, name='rfl'),
    path('arbitraje/', views.arbitraje_rfl, name='arbitraje_rfl'),
    path('arbitraje/llegada', views.llegada_rfl_1, name='llegada_rfl_1'),
    ]

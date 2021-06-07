"""fynsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
#from BASES import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logeado/',views.index),
    path('logeado/hall',views.hall, name='hall'),
    path('logeado/bases/',include('BASES.urls')),
    path('logeado/rfi/',include('RFI.urls')),
    path('logeado/rfl/',include('RFL.urls')),
    path('logeado/rfl/ordenes/',include('ordenes.urls')),
    path('entrada/', views.raiz, name='raiz'), #en esa linea se renderiza la plantilla del login
    path('salida/', views.logout_, name='logout'), #en esa linea logout
    path('login/', views.login_, name='login_'), #procesa el login    
    ]



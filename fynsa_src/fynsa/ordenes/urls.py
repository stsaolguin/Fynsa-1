from django.urls import path
from . import views

urlpatterns = [
    path('ingreso-ordenes-rfi', views.rfi_ingreso_ordenes, name='rfi_ingreso_ordenes'),
    path('listado-ordenes-rfi', views.listado_ordenes, name='listado_ordenes'),
    path('crear-clientes-rfi', views.CrearClienteCreateView.as_view(),name='crear_clientes_rfi'),
    path('listado-bonos-rfi', views.listado_ordenes),
    #path('editar-bonos-rfi', views.listado_ordenes),
    #path('crear-bonos-rfi', views.listado_ordenes),
    path('editar-ordenes-rfi/<int:numero>', views.EditarOrden, name='editar_ordenes'),
    path('borrar-ordenes-rfi/<int:numero>', views.BorrarOrden, name='borrar_ordenes'),
    path('ingreso-ordenes-rfi-arreglo', views.rfi_prueba_arreglo, name='#'),
    path('api/v1/<str:isin>', views.security_name_api, name='api_security_name'),
    path('api/v1/actualiza-status/<str:orden_numero>/<str:estado>', views.actualiza_status, name='actualiza_status'),
    path('listado-ordenes-rfi/papeles', views.busca_papeles, name='buscador_papeles'),
    ]
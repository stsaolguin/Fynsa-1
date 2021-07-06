from django.urls import path
from . import views

urlpatterns = [
    path('ingreso-ordenes-rfi', views.rfi_ingreso_ordenes, name='rfi_ingreso_ordenes'),
    path('ingreso-ordenes-rfi-modelform', views.rfi_ingreso_ordenes_modelform.as_view(), name='rfi_ingreso_ordenes_modelform'),
    path('listado-ordenes-rfi', views.listado_ordenes, name='listado_ordenes'),
    path('crear-clientes-rfi', views.CrearClienteCreateView.as_view(),name='crear_clientes_rfi'),
    path('crear-fondo-odenes', views.ordenes_crea_fondo.as_view(),name='crear_fondo'),
    path('listar-fondo-odenes', views.ordenes_lista_fondos.as_view(),name='listar_fondo'),
    path('editar-fondo-odenes/<pk>', views.ordenes_updatea_fondo.as_view(),name='updatea_fondo'),
    path('borrar-fondo-odenes/<pk>', views.ordenes_borrar_fondo.as_view(),name='borra_fondo'),
    path('salida-fondos', views.salida_fondos,name='salida_fondos'),
    path('listado-bonos-rfi', views.listado_ordenes),
    #path('editar-bonos-rfi', views.listado_ordenes),
    #path('crear-bonos-rfi', views.listado_ordenes),
    path('editar-ordenes-rfi/<pk>', views.ordenes_updatea_orden.as_view(), name='editar_ordenes'),
    path('borrar-ordenes-rfi/<pk>', views.ordenes_borra_orden.as_view(), name='borrar_ordenes'),
    path('ingreso-ordenes-rfi-arreglo', views.rfi_prueba_arreglo, name='#'),
    path('api/v1/<str:isin>', views.security_name_api, name='api_security_name'),
    path('api/v1/actualiza-status/<str:orden_numero>/<str:estado>', views.actualiza_status, name='actualiza_status'),
    path('api/v1/actualiza-status-fondos/<str:orden_numero_fondo>/<str:estatus>', views.actualiza_status_fondo, name='actualiza_status_fondos'),
    path('listado-ordenes-rfi/papeles', views.busca_papeles, name='buscador_papeles'),
    ]
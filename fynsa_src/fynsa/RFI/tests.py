from django.test import TestCase
from RFI.formularios_rfi import IngresoOperacionesRfiBetaIntermediacion

# Create your tests here.
class TestFormulario(TestCase):
    def test_formulario_intermediacion(self):
        datos = {
            'csrfmiddlewaretoken': '7Ack4u8rPnEVvO2Jt2Q8ggwUb7cfENZipZW337N9BGugAXiksjIyLsnOgdXUQ0t2', 
        'formulario': 'intermediacion', 
        'operacion':'compra', #este campo hay que ponerlo hidden
        'papel': 'POWGEN 8 07/17/67',
        'fecha': '2021-12-23', 
        'vendedor': 'ADC MBI', 
        'comprador': 'AFP PORVENIR',
         'cusip': 'PAL3601521E7', #cambiar cusip por isin
         'crncy': 'usd', 
         'country_of_risk': 'AR',
          'factor': '1', 
          'nominales': '500000',
           'mesa': '10', 
           'ejecutivo_precio': '110',
           'cliente_precio':'110', #ver el clienteprecio las logicas de los precios
           'precio_ejecutivo':'110',#ver el clienteprecio las logicas de los precios
           'contraparte':'algo', # ver esta logica
           'ingreso_ejecutivo':'1230' #ver como se calcula
           }
        formulario = IngresoOperacionesRfiBetaIntermediacion(data = datos)
        print(formulario.errors)
        

        

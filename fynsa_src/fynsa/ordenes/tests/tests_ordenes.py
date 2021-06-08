from django.test import SimpleTestCase,Client
from ordenes.formularios_ordenes import rfi_ingreso_orden_formulario
from ordenes.models import rfi_tsox

class TestFormulario(SimpleTestCase):
    def setUp(self):
        self.datos ={
             'cliente' : 'BKR ADC NEVASA',
    'fecha_ingreso':'08/06/2021', 
    'orden_tipo':'cliente compra', 
    'isin' :'US05947LAZ13',
    'papel': 'BRADES 3.2 01/27/25',
    'rating':['IG'], 
    'duracion': ['Toda la curva'],
    'nominales':'5000000',
    'sector' : ['Todos'],
    'precio' :'105,6', 
    'payment_rank' : ['Todos'],
    'ytm' : ['Todos'],
    'notas' : 'Aca vá alguna nota',
    'pais':['BR'],
        }
    
    def test_formulario_ordenes(self):        
        f = rfi_ingreso_orden_formulario(data=self.datos)
        print(f.errors)
        self.assertTrue(f.is_valid())
    
    def test_TsoxModel(self):
        e = rfi_tsox(**self.datos)
        e.save()
        self.assertIs(e.save(),True)


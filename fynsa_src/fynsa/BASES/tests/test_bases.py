from django.test import SimpleTestCase,Client
from BASES.formularios_bases import bases_ingreso_operaciones



class TestFormulario(SimpleTestCase):
    def test_formulario_bases(self):
        datos ={
                'nemo': 'algo',
                'buy': 'TELERENTA - TELERENTA',
                'seller': 'TELERENTA - TELERENTA',
                'fynsa': 'SI',
                'otc_tr': 'OTC',
                #'monto' : '12.3123.123',
                'monto' : '123123123',
                'tasa_buyer' : '0.67',
                'tasa_seller' : '0.68',
                #'compra_depo' : '789.789.789',
                'compra_depo' : '789789789',
                #'venta_depo' : '678.688.687',
                'venta_depo' : '678688687',
                'fecha' : '2021-07-01',
                'tipo_de_pago' : 'PH',
                'fee_buyer_clp' : '120.000',
                'fee_seller_clp' : '130.000',
                #'tasa':'0.68', #este debería ser un valor promedio
                #'valor_final' : '123123123' #este valor debe ser reemplazado por los compra y venta
                #valor final y tasa deben ir, habría que crearlos como valor dummy
                #hay que quitarles el punto a todos los datos menos tasa.
        }
        f = bases_ingreso_operaciones(data=datos)
        #self.assertIn('valor_final',f.errors)
        self.assertTrue(f.is_valid())
        


from django.test import SimpleTestCase,Client,TestCase
from BASES.formularios_bases import bases_ingreso_operaciones_depos,bases_ingreso_operaciones
from BASES.models import bases



class TestFormulario(TestCase):
    '''
    def test_formulario_bases(self):
        datos ={
                'nemo': 'algo',
                'buy': 'TELERENTA - TELER',
                'seller': 'TELERENTA - TELERENTA',
                'fynsa': 'SI',
                'otc_tr': 'OTC',
                #'monto' : '12.3123.123',
                'monto' : '999999999999',
                'tasa_buyer' : '0.6799',
                'tasa_seller' : '0.6899',
                #'compra_depo' : '789.789.789',
                'compra_depo' : '10',
                #'venta_depo' : '678.688.687',
                'venta_depo' : '100',
                'fecha' : '2021-07-01',
                'tipo_de_pago' : 'PH',
                'fee_buyer_clp' : '120.000',
                'fee_seller_clp' : '130.000',
                'dias':'280',
                #'valor_final' : '0' #este valor debe ser reemplazado por los compra y venta
                #valor final y tasa deben ir, habría que crearlos como valor dummy
                #hay que quitarles el punto a todos los datos menos tasa.
        }
        f = bases_ingreso_operaciones(data=datos)
        #self.assertIn('valor_final',f.errors)
        print(f.errors)
        self.assertTrue(f.is_valid())
    '''
    def test_update_result(self):
        datos ={
                'fecha':'2025-01-01',
                'nemo': 'algo',
                'buy': 'TELERENTA - TELER',
                'seller': 'TELERENTA - TELERENTA',
                'fynsa': 'SI',
                'otc_tr': 'OTC',
                'monto' : '12.3123.123',
                'monto' : '999999999999',
                'tasa_buyer' : '0.6799',
                'tasa_seller' : '0.6899',
                'compra_depo' : '789.789.789',
                'compra_depo' : '10',
                'venta_depo' : '678.688.687',
                'venta_depo' : '100',
                'fecha' : '2021-07-01',
                'tipo_de_pago' : 'PH',
                'fee_buyer_clp' : '120',
                'fee_seller_clp' : '130',
                'dias':'280',
                #'valor_final' : '0' #este valor debe ser reemplazado por los compra y venta
                #valor final y tasa deben ir, habría que crearlos como valor dummy
                #hay que quitarles el punto a todos los datos menos tasa.
        }
        obj = bases(**datos)
        obj.save()
        j = bases.objects.filter('fecha').first()
        print(j.fecha)
        # At this point obj.val is still 1, but the value in the database
        # was updated to 2. The object's updated value needs to be reloaded
        # from the database.
        #obj.refresh_from_db()
        self.assertEqual(j.fecha, '2025-01-01')
        


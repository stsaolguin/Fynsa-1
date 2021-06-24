from django.views.generic.edit import ModelFormMixin
from RFI.models import rfi_bonos
from django.test import SimpleTestCase,TestCase
from ordenes.formularios_ordenes import rfi_ingreso_orden_formulario
from ordenes.models import rfi_tsox
import ast
import timeit
from django.test import TestCase,Client
'''
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

'''
'''
class TestBuscadorDePapeles(TestCase):
    """ Este test es para determinar el tiempo de busqueda de papeles """
    def setUp(self):
        #self.paises = ["['BR', 'CL']"]
        #self.sector = ["['Airlines', 'Banking']"]
        #self.rating = ["['IG', 'HY']"]
        #self.duracion = ["['x<=3', '3<x<=5']"]
        #self.ytm = ["['0 a 100', '201 a 300']"]
        #self.payment_rank = ["['1st lien', 'Jr Subordinated']"]
        self.paises = ["['BR']"]
        self.sector = ["['Banco y Financieras']"]
        self.rating = ["['HY']"]
        self.duracion = ["['x<=3', '3<x<=5']"]
        self.ytm = ["['0 a 100','201 a 300']"]
        self.payment_rank = ["['Sr Unsecured']"]

    def test_ObtenerListaUnica(self):
        pr = [d for d in ast.literal_eval(self.paises.pop())]
        sr = [e for e in ast.literal_eval(self.sector.pop())]
        rr = [f for f in ast.literal_eval(self.rating.pop())]
        dr = [g for g in ast.literal_eval(self.duracion.pop())]
        yr = [h for h in ast.literal_eval(self.ytm.pop())]
        pyr = [i for i in ast.literal_eval(self.payment_rank.pop())]
        print(pr)
        resultado = []
        comienzo = timeit.timeit()
        for r in rr:
            for s in pr:
                print(s)
                for t in sr:
                    for u in dr:
                        for v in yr:
                            for w in pyr:
                                print(r,s,t,u,v,w)
                                busqueda = rfi_bonos.objects.filter(risk=r,cntry_of_risk=s,industria=t,dur_text=u,yas_bond_text=v,payment_rank=w)
                                print(busqueda)
                                if busqueda.exists():
                                    resultado.append(busqueda)
        final = timeit.timeit()
        print(resultado)
        print("tiempo total  : ",final-comienzo)

        
        self.assertEqual(True,True)
        


'''

from django.urls import reverse
from ordenes.views import rfi_ingreso_ordenes_modelform
from fynsa.views import login_
class TesteoUrls(TestCase):
    def test_urls(self):
        c = Client()
        url = reverse('rfi_ingreso_ordenes_modelform')
        url_login = reverse('login_')
        log = c.post(url_login, {'usr':'gvera','pasw':'gonzalovera26'})
        res = c.get(url)
        print('************* Contenido ',res.content)
        self.assertEqual(log.status_code,200)
from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from BASES.views import *



class TestDetallesClientes(SimpleTestCase):

    def test_detalles_clientes(self):
        url = reverse('bases')
        print(resolve(url))
        self.assertAlmostEquals(resolve(url).func,comite_bases)

# Create your tests here.


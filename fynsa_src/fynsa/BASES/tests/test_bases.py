from django.test import TestCase,SimpleTestCase,Client
from django.urls import reverse
from BASES.urls import *
from fynsa.urls import *
from django.contrib.auth.models import User
from BASES.models import bases




class TestDetallesClientes(TestCase):

    def setUp(self):
        self.credenciales = {
            'username' : 'prueba_nombre',
            'password' : 'prueba_pass',
            'email' : 'prueba_correo'
            }
        User.objects.create_user(**self.credenciales)
        #self.usuario = User.objects.create_user(**self.credenciales)
        
        
    def test_refrescar_base(self):
        nueva_linea = bases.objects.create(
            fecha='2021-02-22',
            otc_tr = 'OTC',
            nemo = 'algo'

        )
        c = Client()
        usuario = c.login(**self.credenciales)
        h = c.get(reverse('bases'),follow=True)
        h.user = usuario
        self.assertContains(h,'<input type="date" name="fecha_final" value="2021-02-22" class="form-control mx-2" required id="id_fecha_final">',html=True)
       
# Create your tests here.


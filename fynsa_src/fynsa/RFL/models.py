from django.db import models
from BASES.models import *
import settings


class tr(models.Model):
    instrumento = models.TextField()
    tipo = models.TextField()
    cantidad = models.BigIntegerField()
    reajuste = models.TextField()
    tir_media = models.DecimalField(max_digits=5,decimal_places=2)
    duracion = models.DecimalField(max_digits=5,decimal_places=2)
    rating = models.TextField()
    rol_tr = models.TextField(default="color:red")

    def save(self,*args,**kargs):
        if self.reajuste=='$':
            self.reajuste="CLP"
        
        super().save(*args,**kargs)


class risk(models.Model):
    nemo = models.TextField()
    tipo = models.TextField()
    riesgo = models.TextField()
    moneda = models.TextField()
    monto_outstanding = models.BigIntegerField() #este monto debe ser <>0
    duracion = models.DecimalField(max_digits=5, decimal_places=2)
    tir = models.DecimalField(max_digits=5, decimal_places=2)
    rol_rsk = models.TextField(default="color:green")

    def save(self,*args,**kargs):
        if float(self.tir) > float(100):
            self.tir=100
        if self.monto_outstanding=='':
            self.monto_outstanding=0
        super().save(*args,**kargs)


class lva(models.Model):
    nemo = models.TextField()
    tipo = models.TextField()
    unidad_reaj = models.CharField(max_length=3)
    precio = models.DecimalField(max_digits=8, decimal_places=5)
    plazo_economico = models.IntegerField()
    tir_val = models.DecimalField(max_digits=6, decimal_places=4)
    tir_transa = models.DecimalField(max_digits=4,decimal_places=3)
    categoria = models.CharField(max_length=2)
    
# aca iría los mdelos de arbitraje y la hd.
class hd(models.Model):
    fecha = models.DateField(null=True)
    cliente = models.ForeignKey(clientes,on_delete=models.CASCADE,null=True)
    monto = models.BigIntegerField(null=True,default=0)
    operador = models.ForeignKey(operador,on_delete=models.CASCADE,null=True)

class posiciones(models.Model):
    fuente_del_instrumento = models.TextField(null=True,blank=True)
    institucion = models.TextField(null=True,blank=True)
    nemotecnico = models.TextField(null=True,blank=True)
    valor_nominal = models.BigIntegerField(null=True,blank=True)
    marca = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    dur_rskam = models.DecimalField(max_digits=5,decimal_places=3,null=True,blank=True)
    maturity = models.DateField(null=True,blank=True)
    tipo_instrumento = models.TextField(null=True,blank=True)
    crncy = models.TextField(null=True,blank=True)
    fecha_subida=models.DateField(auto_now=True,null=True,blank=True)

class clientes_rfl(models.Model):
    cliente = models.TextField()

class operador(models.Model):
    operador = models.TextField()

class hd_aux(models.Model):
    fecha = models.DateField(null=True)
    cliente = models.TextField()
    monto = models.BigIntegerField(null=True,default=0)
    operador = models.TextField()
    
class archivos_cintas(models.Model):
    tr = models.FileField(upload_to='cintas/')
    rsk = models.FileField(upload_to='cintas/')

class bonos(models.Model):
    ''' Este modelo se usa para sacar el riesgo de los bonos y usarlos en cintas '''
    instrumento = models.TextField()
    rating = models.TextField()
    tipo = models.TextField(default='')

class actividad(models.Model):
    '''Este modelo es para poner fecha de ultima subida y timestamp '''
    name = models.TextField()
    accion = models.TextField()
    usuario = models.TextField()
    fecha = models.DateTimeField(auto_now=True)



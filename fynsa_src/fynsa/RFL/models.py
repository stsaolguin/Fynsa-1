from django.db import models
from BASES.models import *
import settings

class tr(models.Model):
    instrumento = models.TextField()
    tipo = models.TextField()
    cantidad = models.IntegerField()
    reajuste = models.TextField()
    tir_media = models.DecimalField(max_digits=5,decimal_places=2)
    duracion = models.DecimalField(max_digits=5,decimal_places=2)
    rating = models.TextField()


class risk(models.Model):
    nemo = models.TextField()
    tipo = models.TextField()
    riesgo = models.TextField()
    moneda = models.TextField()
    monto_outstanding = models.BigIntegerField() #este monto debe ser <>0
    duracion = models.DecimalField(max_digits=5, decimal_places=2)
    tir = models.DecimalField(max_digits=5, decimal_places=2)

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
    fuente_del_instrumento = models.TextField(choices=[('AFP','AFP'),('FFMM','FFMM'),('FIP','FIP'),('FNR','FNR'),('FYNSA','FYNSA'),('SEG_G','SEG_G'),('SEG_V','SEG_V')])
    institucion = models.TextField()
    nemotecnico = models.TextField()
    valor_nominal = models.BigIntegerField()
    marca = models.DecimalField(max_digits=4,decimal_places=2)
    dur_rskam = models.DecimalField(max_digits=5,decimal_places=3)
    maturity = models.DateField()
    tipo_instrumento = models.TextField()
    crncy = models.TextField()
    fecha_subida=models.DateField(default='0')

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



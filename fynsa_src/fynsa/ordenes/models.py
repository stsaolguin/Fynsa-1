from django.db import models
from django.contrib.postgres.fields import ArrayField
from BASES.models import ejecutivos

class rfi_tsox(models.Model):
	fecha_ingreso = models.DateField()
	trader = models.TextField(null=True,blank=True) #Este campo se va a poner solo en función de quién está logeado
	orden_tipo = models.TextField(null=True,blank=True)
	isin = models.TextField(null=True,blank=True)
	papel = models.TextField(null=True,blank=True)
	cliente = models.TextField(null=True,blank=True)
	rating = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	pais = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	duracion = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	nominales = models.BigIntegerField(null=True,blank=True)
	sector = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	precio = models.DecimalField(max_digits=6,decimal_places=3,null=True,blank=True)
	payment_rank = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	ytm = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	notas = models.TextField(null=True,blank=True)
	status = models.TextField(null=True,blank=True)

class rfi_tsox_borrado(models.Model):
	fecha_ingreso = models.DateField()
	trader = models.TextField(null=True,blank=True) #Este campo se va a poner solo en función de quién está logeado
	orden_tipo = models.TextField(null=True,blank=True)
	isin = models.TextField(null=True,blank=True)
	papel = models.TextField(null=True,blank=True)
	cliente = models.TextField(null=True,blank=True)
	rating = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	pais = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	duracion = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	nominales = models.BigIntegerField(null=True,blank=True)
	sector = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	precio = models.DecimalField(max_digits=6,decimal_places=3,null=True,blank=True)
	payment_rank = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	ytm = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	notas = models.TextField(null=True,blank=True)
	status = models.TextField(null=True,blank=True)

class fondo(models.Model):
	nombre_fondo = models.TextField(null=True,blank=True)
	duracion_fondo = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	sector_fondo = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	ytm_fondo = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	risk_fondo = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	cntry_of_risk_fondo = ArrayField(models.CharField(max_length=100),null=True,blank=True)
	trader_fondo = models.TextField(null=True,blank=True)#trader externo, contraparte
	tamano_fondo = models.BigIntegerField(null=True,blank=True,default=0)
	pais_fondo = models.TextField(null=True,blank=True)
	notas_fondo = models.TextField(null=True,blank=True)
	ejecutivo = models.ForeignKey(ejecutivos,on_delete=models.CASCADE)

class fondo_salida(models.Model):
	orden_asignada = models.ForeignKey(rfi_tsox,on_delete=models.CASCADE)
	fondo_asignado = models.ForeignKey(fondo,on_delete=models.CASCADE)
	status_asignado = models.TextField(null=True,blank=True)
	notas_asignado = models.TextField(null=True,blank=True)

class intenciones_pasadas_salida(models.Model):
	orden_asignada = models.ForeignKey(rfi_tsox,on_delete = models.CASCADE)
	intencion_pasada_asignada = models.ForeignKey(rfi_tsox_borrado,on_delete = models.CASCADE)
	status_intencion_asignada = models.TextField(null = True, blank= True)
	notas_intencion_asignada = models.TextField(null = True, blank= True)

class carteras_bbg(models.Model):
	fondo = models.TextField(null=True,blank=True)
	sector = models.TextField(null=True,blank=True)
	nemo  = models.TextField(null=True,blank=True)
	weight = models.DecimalField(null=True,blank=True,max_digits=6,decimal_places=3)
	mkt_val = models.BigIntegerField(null=True,blank=True) 
	pos_val = models.BigIntegerField(null=True,blank=True) # a este campo hay que truncarle los decimales
	px_close = models.DecimalField(null=True,blank=True,max_digits=6,decimal_places=3) 
	crncy = models.TextField(null=True,blank=True)
	isin = models.TextField(null=True,blank=True)
	ejecutivo = models.TextField(null=True,blank=True)
 
	
class holders_salida(models.Model):
	orden_asignada = models.ForeignKey(rfi_tsox,on_delete = models.CASCADE)
	holder_asignada = models.ForeignKey(carteras_bbg,on_delete = models.CASCADE)
	status_holder_asignada = models.TextField(null = True, blank= True)
	notas_holder_asignada = models.TextField(null = True, blank= True)
	

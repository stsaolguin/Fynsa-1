from django.db import models

# Create your models here.
class rfi_beta(models.Model):
    linea=models.AutoField(primary_key=True)
    fecha = models.DateField()
    ejecutivo = models.CharField(max_length=7,null=True)
    papel = models.TextField()
    cusip = models.TextField(null=True)
    operacion = models.TextField(choices=[('venta','venta'),('compra','compra')])
    nominales = models.IntegerField()
    mesa = models.DecimalField(max_digits=7, decimal_places=3,null=True)
    ejecutivo_precio = models.DecimalField(max_digits=7, decimal_places=2, default=0,null=True)
    cliente_precio = models.DecimalField(max_digits=7, decimal_places=2, default=0,null=True)
    ingreso_ejecutivo = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    ingreso_mesa = models.DecimalField(max_digits=9, decimal_places=2,null=True)
    contraparte = models.TextField()
    spread_mesa = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    comprador = models.TextField()
    vendedor = models.TextField()
    country_of_risk = models.CharField(max_length=5, null=True)
    crncy = models.CharField(max_length=5,null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=3, default=00.000, null=True, blank=True)
    tipo_de_cambio = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    fecha_subido = models.DateTimeField(auto_now=True, null=True)
    

    def __str__(self):
        return str(self.fecha)


class bonos_rfi(models.Model):
    #esta class es para los datos del informe spread
    cusip = models.TextField(primary_key=True)
    duration = models.DecimalField(max_digits=5, decimal_places=3,default=0,null=True,blank=True)
    papel = models.TextField(null=True,blank=True)
    industry_sector = models.TextField(default='-',null=True,blank=True)
    industry_group = models.TextField(default='-',null=True,blank=True)
    cntry_of_risk = models.CharField(max_length=2,default='-',null=True,blank=True)
    industria = models.TextField(default='-',null=True,blank=True)
    risk = models.TextField(default='',null=True,blank=True)
    tasa = models.IntegerField(default='',null=True,blank=True)
    fecha_subida = models.DateField(null=True,blank=True)
    maturity = models.DateField(null=True,blank=True)
    
class clientes_rfi(models.Model):
    fondo = models.TextField(null=True,blank=True)
    nombre_cliente = models.TextField(unique=True,null=True,blank=True)
    categoria = models.TextField(null=True,blank=True)
    pais = models.CharField(max_length=3,null=True,blank=True)
    operador_fynsa = models.TextField(null=True,blank=True)
    activo = models.BooleanField(default=True,null=True,blank=True)
    prospecto = models.BooleanField(default=False,null=True,blank=True)
    trader_contraparte = models.TextField(null=True,blank=True)
    final = models.BooleanField(null=True,blank=True,default='t')
    categoria_fynsa = models.TextField(null=True,blank=True)


class rfi_generacion_historica(models.Model):
    fecha = models.DateField(null=True,blank=True)
    pais = models.CharField(max_length=3,null=True,blank=True)
    categoria = models.TextField(null=True,blank=True)
    nombre_cliente = models.TextField(null=True,blank=True)
    generacion = models.IntegerField(null=True,blank=True)
    spread = models.DecimalField(max_digits=5, decimal_places=3, null=True)


class rfi_generacion_comite_temporal(models.Model):
    pais = models.CharField(max_length=3,null=True,blank=True)
    categoria = models.TextField(null=True,blank=True)
    nombre_cliente = models.TextField(null=True,blank=True)
    generacion_brk = models.IntegerField(null=True,blank=True)
    generacion_finales = models.IntegerField(null=True,blank=True)
    generacion_bancos_brk = models.IntegerField(null=True,blank=True)
    generacion_total = models.IntegerField(null=True,blank=True)
    spread_brk = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    spread_finales = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    spread_banco_brk = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    generacion_brk_t_1 = models.IntegerField(null=True,blank=True)
    generacion_finales_t_1 = models.IntegerField(null=True,blank=True)
    generacion_bancos_brk_t_1 = models.IntegerField(null=True,blank=True)
    generacion_total_t_1 = models.IntegerField(null=True,blank=True)









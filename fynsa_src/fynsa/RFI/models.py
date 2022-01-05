from RFL.models import risk
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class rfi_beta(models.Model):
    linea=models.AutoField(primary_key=True)
    fecha = models.DateField()
    ejecutivo = models.CharField(max_length=7,null=True)
    cliente = models.TextField(blank = True,null=True)
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
    factor = models.DecimalField(max_digits=22, decimal_places=20, default=1.00000000000000000000,null=True,blank=True)
    ejecutivo_bp_nombre = models.TextField(blank = True,null=True)
    
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



class rfi_bonos(models.Model):
    #esta class es para los datos del sistema de posiciones
    cusip = models.TextField(null=True,blank=True)
    security_name = models.TextField(null=True,blank=True)
    short_name = models.TextField(null=True,blank=True)
    bb_composite = models.CharField(max_length=4,default='NR',null=True,blank=True)
    payment_rank = models.CharField(max_length=40,null=True,blank=True)
    cntry_of_risk = models.CharField(max_length=2,null=True,blank=True)
    yas_mod_dur = models.DecimalField(max_digits=7, decimal_places=3,default=0,null=True,blank=True)
    yas_bond_yld = models.DecimalField(max_digits=7, decimal_places=3,default=0,null=True,blank=True)
    classification = models.TextField(default='-',null=True,blank=True)
    industria = models.TextField(null=True,blank=True)
    ising = models.TextField(null=True,blank=True)
    risk = models.TextField(default='NR',null=True,blank=True)
    dur_text = models.TextField(null=True,blank=True)
    tasa = models.IntegerField(default='',null=True,blank=True)
    fecha_subida = models.DateField(null=True,blank=True)
    maturity = models.DateField(null=True,blank=True)
    yas_bond_porcentaje = models.DecimalField(max_digits=9, decimal_places=3,default=0,null=True,blank=True)
    yas_bond_text = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.short_name
        
    def save(self,*args, **kwargs):
        var_aux_list = self.yas_bond_yld
        var_aux = var_aux_list[0]
        self.yas_bond_porcentaje = float(var_aux) * 100

        if self.yas_bond_porcentaje > 400.000:
            self.yas_bond_text = 'sobre 401'
        elif self.yas_bond_porcentaje > 300.000:
            self.yas_bond_text = '301 a 400'
        elif self.yas_bond_porcentaje > 200.000:
            self.yas_bond_text = '201 a 300'
        elif self.yas_bond_porcentaje > 100.000:
            self.yas_bond_text = '101 a 200'
        elif self.yas_bond_porcentaje <= 100.000:
            self.yas_bond_text = '0 a 100'
        
        var_aux_list_2 = self.yas_mod_dur
        if isinstance(var_aux_list_2,list):
           var_aux2 = float(var_aux_list_2[0])
        else:
           var_aux2 = float(var_aux_list_2)

        if var_aux2 > 5.00:
            self.dur_text = 'x>5'
        elif var_aux2 > 3.00:
            self.dur_text = '3<x<=5'
        elif var_aux2 <= 3.00:
            self.dur_text = 'x<=3'
        
        self.tasa = 0 if self.tasa=='' else self.tasa
        
        super(rfi_bonos,self).save(*args, **kwargs)



class PruebaArrayModel(models.Model):
    riesgo = ArrayField(models.CharField(max_length=100, blank=True))
    
class ejecutivos_externos_bp(models.Model):
    nombre_completo = models.TextField(blank=True,null=True)
    codigo = models.CharField(max_length=3,null=True,blank=True)
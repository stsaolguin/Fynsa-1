from django.db import models

# Create your models here.

class operador(models.Model):
    nombre_operador = models.TextField(primary_key=True)
    abreviatura = models.CharField(max_length=4)
    mesa = models.TextField(choices=[('RFL','Local'),('RFI','Internacional'),('BASES','Bases')])
    activo = models.BooleanField(default=True)

class clientes(models.Model):
    nombre = models.TextField(default='',null=True)
    nacionalidad_cliente = models.TextField(null=True, blank=True)
    operador_fynsa = models.ForeignKey(operador,on_delete=models.CASCADE, default='',null=True, blank=True)
    categoria = models.TextField(null=True, blank=True)
    operador_contraparte = models.TextField(null=True, blank=True)
    esta_activo = models.BooleanField(default=True,null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    email_cco = models.TextField(null=True, blank=True)
    factura = models.BooleanField(default=False, blank=True)
    cliente_principal = models.TextField(default='',null=True, blank=True)
    anidado = models.BooleanField(default=False, blank=True)

    
    def __str__(self):
        return self.nombre

class bases(models.Model):
    linea = models.AutoField(primary_key=True)
    fecha = models.DateField()
    fynsa = models.TextField(choices=[('NO','NO'),('SI','SI')], null=True,blank=True)
    otc_tr = models.TextField(choices=[('OTC','OTC'),('TR','TR')],null=True,blank=True)
    nemo = models.TextField()
    dias = models.IntegerField(null=True, default=0)
    monto = models.BigIntegerField(null=True, default=0)
    tipo_de_pago = models.TextField(choices=[('PM','PM'),('PH','PH'),('CN','CN')],null=True,blank=True)
    buy = models.TextField()
    seller = models.TextField()
    trader_buy = models.TextField(null=True, default=0)
    trader_seller = models.TextField(null=True, default=0)
    tasa = models.DecimalField(max_digits=4, decimal_places=2,null=True)
    valor_final = models.BigIntegerField(null=True, default=0)
    fee_buyer = models.IntegerField(null=True, default=0)
    fee_seller = models.IntegerField(null=True, default=0)
    fee_buyer_moneda = models.TextField(choices=[('CLP','CLP'),('USD','USD')],null=True)
    fee_seller_moneda = models.TextField(choices=[('CLP','CLP'),('USD','USD')],null=True)
    compra_depo = models.BigIntegerField(null=True, default=0)
    venta_depo = models.BigIntegerField(null=True, default=0)
    util_depo = models.BigIntegerField(null=True, default=0)
    valor_clp = models.BigIntegerField(null=True, default=0)
    fee_buyer_clp = models.IntegerField(null=True, default=0)
    fee_seller_clp = models.IntegerField(null=True, default=0)
    participante_1 = models.TextField(null=True)
    participante_2 = models.TextField(null=True)
    tipo_de_cambio = models.DecimalField(max_digits=5, decimal_places=2,null=True, default=0)
    uf = models.DecimalField(max_digits=7, decimal_places=2,null=True, default=0)
    concate = models.TextField(null=True)
    institucion_trader_buyer = models.TextField(null=True)
    institucion_trader_seller = models.TextField(null=True)
    institucion_trader_participante_1 = models.TextField(null=True)
    institucion_trader_participante_2 = models.TextField(null=True)
    tasa_buyer = models.DecimalField(max_digits=4, decimal_places=2,null=True)
    tasa_seller = models.DecimalField(max_digits=4, decimal_places=2,null=True)
        

    def __str__(self):
        return str(self.fecha)

class facturas_bases(models.Model):
    linea = models.AutoField(primary_key=True)
    folio_factura = models.IntegerField(null=True, default=0, unique=True)
    cliente = models.TextField(null=True, default=0)
    fecha_emision = models.DateField()
    monto_neto = models.BigIntegerField(null=True, default=0)
    monto_total = models.BigIntegerField(null=True, default=0)
    def __str__(self):
        return str(self.fecha_emision)

class serie_generacion_total_diaria(models.Model):
    fecha = models.DateField()
    cliente = models.TextField()
    total_consolidada = models.BigIntegerField()

class serie_generacion_mensual(models.Model):
    fecha = models.DateField(null=True, blank=True)
    monto_bases = models.BigIntegerField(null=True, blank=True)
    monto_depositos = models.BigIntegerField(null=True, blank=True)
    monto_total = models.BigIntegerField(null=True, blank=True)
    monto_meta = models.BigIntegerField(null=True, blank=True)
    clientes_80 = models.IntegerField(null=True, blank=True)
    clientes_activos = models.IntegerField(null=True, blank=True)

class serie_montos_mensual_por_cliente(models.Model):
    fecha = models.DateField(null=True, blank=True)
    cliente = models.TextField(null=True, default='')
    monto_bases_otc = models.BigIntegerField(null=True, blank=True)
    monto_bases_tr = models.BigIntegerField(null=True, blank=True)
    monto_depos_otc = models.BigIntegerField(null=True, blank=True)
    monto_depos_tr = models.BigIntegerField(null=True, blank=True)
    monto_total = models.BigIntegerField(null=True, blank=True)

class serie_generacion_mensual_por_cliente(models.Model):
    fecha = models.DateField(null=True, blank=True)
    cliente = models.TextField(null=True, default='')
    gen_depo = models.BigIntegerField(null=True, blank=True)
    gen_bases = models.BigIntegerField(null=True, blank=True)
    prov_bases = models.BigIntegerField(null=True, blank=True)
    prov_depos = models.BigIntegerField(null=True, blank=True)
    
class cliente_trader(models.Model):
    institucion_trader = models.TextField(null=True)


from RFL.models import risk
from django.db import models
from django.contrib.postgres.fields import ArrayField

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

    def __str__(self):
        return self.short_name
        
    def save(self,*args, **kwargs):
        categorias = {
        'Food and Beverage':'Retail',
        'Midstream':'O&G',
        'Independent':'O&G',
        'Natural Gas':'O&G',
        'Papper' : 'Pulpa y Papel',
        'Airlines' : 'Aerolineas',
        'Aerospace/Defense' : 'Aerolineas',
        'Banking':'Banco y Financieras',
        'Brokerage Assetmanagers Exchanges':'Banco y Financieras',
        'Other Financial':'Banco y Financieras',
        'Finance Companies':'Banco y Financieras',
        'Government Owned, No Guarantee':'Quasisov',
        'Goverment Sponsored':'QuasiSov',
        'Electric' : 'Utilities',
        'Local Authority' : 'Utilities',
        'Wireless' : 'Telecom',
        'Wirelines' : 'Telecom',
        'Media Entertainment' : 'Telecom',
        'Cable Satellite' : 'Telecom',
        'Railroads' : 'Transporte',
        'Transportation Services' : 'Transporte',
        'Metal and Mining':'Mineria y Minerales',
        'Chemicals':'Químicos',
        'Building Materials':'Cemento y Construcción',
        'Other Industrial':'Real State',
        'Retailers':'Retail',
        'Gaming':'Retail',
        'Consumer Products':'Retail',
    }
        risk_dic ={
            'AAA':'IG',
            'AAA-':'IG',
            'AA':'IG',
            'AA+':'IG',
            'AA-':'IG',
            'A':'IG',
            'A+':'IG',
            'A-':'IG',
            'BBB':'IG',
            'BBB+':'IG',
            'BBB-':'HY',
            'BB':'HY',
            'BB+':'HY',
            'BB-':'HY',
            'B':'HY',
            'B+':'HY',
            'B-':'HY',
            'CCC':'HY',
            'CCC+':'HY',
            'CCC-':'HY',
            'CC':'HY',
            'CC+':'HY',
            'CC-':'HY',
            'C':'HY',
            'C+':'HY',
            'C-':'HY',
            'DDD':'HY',
            'DDD+':'HY',
            'DDD-':'HY',
            'DD':'HY',
            'DD+':'HY',
            'DD-':'HY',
            'D':'HY',
            'D+':'HY',
            'D-':'HY',
            
        }
        cat = categorias[self.classification] or None
        self.industria = cat
        r = risk_dic[self.bb_composite] or 'NR'
        self.dur_text = r
        super().save(*args, **kwargs)



class PruebaArrayModel(models.Model):
    riesgo = ArrayField(models.CharField(max_length=100, blank=True))



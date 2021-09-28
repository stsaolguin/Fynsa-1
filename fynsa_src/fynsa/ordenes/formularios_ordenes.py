from django.db.models.expressions import F, OrderBy
from ordenes.models import rfi_tsox,fondo
from django import forms
from django.forms import ModelForm, fields
from RFI.models import clientes_rfi,rfi_bonos
from BASES.models import ejecutivos
import datetime
from django.core.exceptions import ValidationError

#estas listas son las que se usan para buscar si están todos los ítemes dentro de las listas pais,sector,etc.
#Si 
l_sector = [x.industria for x in rfi_bonos.objects.all().distinct('industria')]
l_paymentRank = [x.payment_rank for x in rfi_bonos.objects.all().distinct('payment_rank')]
l_cntry = [x.cntry_of_risk for x in rfi_bonos.objects.all().distinct('cntry_of_risk')]
l_rating = ['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-','BB+','BB','BB-','B+','B','B-','CCC+','CCC','CCC-','CC','C','D','NR']
l_duracion = ['x<=3','3<x<=5','x>5']
l_ytm = ['0 a 100','101 a 200','201 a 300','301 a 400','sobre 401']

####
def lista_sector():
    listado = [(x.industria,x.industria) for x in rfi_bonos.objects.all().distinct('industria')]
    listado.insert(0,('Todos','Todos'))
    return listado

def lista_paymentRank():
    listado = [(x.payment_rank,x.payment_rank) for x in rfi_bonos.objects.all().distinct('payment_rank')]
    listado.insert(0,('Todos','Todos'))
    return listado

def listado_isin():
    return [(x.ising,x.ising) for x in rfi_bonos.objects.all().distinct('ising')]

def listado_cntry():
    listado = [(x.cntry_of_risk,x.cntry_of_risk) for x in rfi_bonos.objects.all().distinct('cntry_of_risk')]
    listado.insert(0,('Todos','Todos'))
    return listado
def listado_ratings():
    listado = [('Todos','Todos'),('AAA','AAA'),('AA+','AA+'),('AA','AA'),('AA-','AA-'),('A+','A+'),('A','A'),('A-','A-'),('BBB+','BBB+'),('BBB','BBB'),('BBB-','BBB-'),('BB+','BB+'),('BB','BB'),('BB-','BB-'),('B+','B+'),('B','B'),('B-','B-'),('CCC+','CCC+'),('CCC','CCC'),('CCC-','CCC-'),('CC','CC'),('C','C'),('D','D'),('NR','NR')]
    return listado
    
def dia_actual():
    return datetime.date.today()

def listado_ejecutivos(mesa):
    return ejecutivos.objects.filter(mesa=mesa).order_by('ejecutivo')

class AgregaClientes(ModelForm):
    def __init__(self,*args, **kwargs):
        super(AgregaClientes,self).__init__(*args, **kwargs)
        self.fields['fondo'].widget.attrs = {'class':'form-control'}
        self.fields['final'].widget.attrs = {'class':'form-control'}
        self.fields['categoria'].widget.attrs = {'class':'form-control'}
        self.fields['pais'].widget.attrs = {'class':'form-control'}

    class Meta:
        model = clientes_rfi
        fields = ['fondo','final','categoria','pais']

class IngresoOrdenesRFIModelForm(ModelForm):
    def __init__(self,*args, **kwargs):
        super(IngresoOrdenesRFIModelForm,self).__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].widget.attrs = {'class':'form-control','type':'date'}
        self.fields['orden_tipo'].widget.attrs = {'class':'form-control'}
        self.fields['nominales'].widget.attrs = {'class':'form-control'}
        self.fields['precio'].widget.attrs = {'class':'form-control'}
        self.fields['papel'].widget.attrs = {'class':'form-control'}
        self.fields['rating'].widget.attrs = {'class':'form-control'}
        self.fields['duracion'].widget.attrs = {'class':'form-control'}
        self.fields['payment_rank'].widget.attrs = {'class':'form-control'}
        self.fields['ytm'].widget.attrs = {'class':'form-control'}
        self.fields['sector'].widget.attrs = {'class':'form-control'}
        self.fields['notas'].widget.attrs = {'class':'form-control'}
        self.fields['pais'].widget.attrs = {'class':'form-control'}
        self.fields['cliente'].widget.attrs = {'class':'form-control'}
        self.fields['isin'].widget.attrs = {'class':'form-control'}
        self.fields['cliente'].choices = [(x.nombre_fondo,x.nombre_fondo) for x in fondo.objects.all().order_by('nombre_fondo')]
        self.fields['isin'].choices = listado_isin()
        
    cliente = forms.ChoiceField()
    fecha_ingreso = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type':'date'}),initial = dia_actual())
    orden_tipo = forms.ChoiceField(choices = [('cliente compra','cliente compra'),('cliente vende','cliente vende')])
    isin = forms.ChoiceField(required=False)
    papel = forms.CharField(required=False)
    rating = forms.MultipleChoiceField(choices = listado_ratings(),initial='Todos',required=False)
    duracion = forms.MultipleChoiceField(choices=[('Toda la curva','Toda la curva'),('x<=3','x<=3'),('3<x<=5','3<x<=5'),('x>5','x>5')],initial='Toda la curva',required=False)
    nominales = forms.CharField(required=False)
    sector = forms.MultipleChoiceField(choices=lista_sector(),initial='Todos',required=False)
    precio = forms.CharField(required=False)
    payment_rank = forms.MultipleChoiceField(choices=lista_paymentRank(),initial='Todos',required=False)
    ytm = forms.MultipleChoiceField(choices=[('Todos','Todos'),('0 a 100','0 a 100'),('101 a 200','101 a 200'),('201 a 300','201 a 300'),('301 a 400','301 a 400'),('sobre 401','sobre 401')],initial='Todos',required=False)
    notas = forms.CharField(required=False)
    pais = forms.MultipleChoiceField(choices = listado_cntry(),initial='Todos',required=False) 
    class Meta:
        model = rfi_tsox
        fields = ('cliente','fecha_ingreso','orden_tipo','nominales','precio','papel','rating','duracion','payment_rank','ytm',
        'sector','notas','pais','isin')
        
    def clean_nominales(self):
        nominales = self.cleaned_data['nominales']
        nominales = nominales.replace('.','').replace(',','.')
        if nominales=='':
            raise ValidationError('Falta el campo nominales.')
        else:
            return nominales            

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        precio = precio.replace(',','.')
        if precio == '':
            return 0
        else:
            return precio
                    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if 'Todos' in rating:
            return ['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-','BB+','BB','BB-','B+','B','B-','CCC+','CCC','CCC-','CC','C','D','NR']
        else:
            return rating
    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        if 'Toda la curva' in duracion:
            return ['x<=3','3<x<=5','x>5']
        else:
            return duracion
    def clean_sector(self):
        sector = self.cleaned_data['sector']
        if 'Todos' in sector:
            return [x.industria for x in rfi_bonos.objects.all().distinct('industria')]
        else:
            return sector
    def clean_payment_rank(self):
        payment_rank = self.cleaned_data['payment_rank']
        if 'Todos' in payment_rank:
            return [x.payment_rank for x in rfi_bonos.objects.all().distinct('payment_rank')]
        else:
            return payment_rank

    def clean_ytm(self):
        ytm = self.cleaned_data['ytm']
        if 'Todos' in ytm:
            return ['0 a 100','101 a 200','201 a 300','301 a 400','sobre 401']
        else:
            return ytm
    def clean_pais(self):
        pais = self.cleaned_data['pais']
        if 'Todos' in pais:
            return [x.cntry_of_risk for x in rfi_bonos.objects.all().distinct('cntry_of_risk')]
        else:
            return pais

class FondoOrdenes(ModelForm):
    def __init__(self,*args,**kwargs):
        super(FondoOrdenes,self).__init__(*args,**kwargs)
        self.fields['nombre_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['duracion_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['sector_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['ytm_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['risk_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['cntry_of_risk_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['trader_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['tamano_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['notas_fondo'].widget.attrs = {'class':'form-control'}
        self.fields['ejecutivo'].widget.attrs = {'class':'form-control'}
        self.fields['pais_fondo'].widget.attrs = {'class':'form-control','placeholder':'Nomenclatura Bloomberg'}
        self.fields['ticker_fondo'].widget.attrs = {'class':'form-control','placeholder':'ej.- CCLACDI Equity'}
        self.fields['email_fondo'].widget.attrs = {'class':'form-control','placeholder':'algo@ejemplo.com'}

    
    nombre_fondo = forms.CharField(label="Nombre Fondo")
    duracion_fondo = forms.MultipleChoiceField(choices=[('Toda la curva','Toda la curva'),('x<=3','x<=3'),('3<x<=5','3<x<=5'),('x>5','x>5')],initial='Toda la curva',required=False)
    sector_fondo = forms.MultipleChoiceField(choices=lista_sector(),initial='Todos',required=False)
    ytm_fondo = forms.MultipleChoiceField(choices=[('Todos','Todos'),('0 a 100','0 a 100'),('101 a 200','101 a 200'),('201 a 300','201 a 300'),('301 a 400','301 a 400'),('sobre 401','sobre 401')],initial='Todos',required=False)
    risk_fondo = forms.MultipleChoiceField(choices =listado_ratings(),initial='Todos',required=False)
    cntry_of_risk_fondo = forms.MultipleChoiceField(choices = listado_cntry(),initial='Todos',required=False) 
    trader_fondo = forms.CharField(label='Trader del fondo (Ellos)',required=False)
    tamano_fondo = forms.CharField(label='Tamaño del fondo (en Millones).',required=False)
    notas_fondo = forms.CharField(required=False)
    pais_fondo = forms.CharField(required=False)
    ticker_fondo = forms.CharField(required=False)
    email_fondo = forms.CharField(required=False)
    ejecutivo = forms.ModelChoiceField(label='Ejecutivo del fondo (Nosotros)',queryset=listado_ejecutivos('RFI'))

    #acá habría que poner un metodo para limpiar el tamaño del fondo. Si viene vacío, asume 0.
    class Meta:
        model = fondo
        fields = '__all__'

    def clean_tamano_fondo(self):
        tamano_fondo = self.cleaned_data['tamano_fondo']
        if tamano_fondo == '':
            return 0
        else:
            return tamano_fondo
    def clean_risk_fondo(self):
        rating = self.cleaned_data['risk_fondo']
        if 'Todos' in rating:
            return ['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-','BB+','BB','BB-','B+','B','B-','CCC+','CCC','CCC-','CC','C','D','NR']
        else:
            return rating
    def clean_duracion_fondo(self):
        duracion = self.cleaned_data['duracion_fondo']
        if 'Toda la curva' in duracion:
            return ['x<=3','3<x<=5','x>5']
        else:
            return duracion
    def clean_sector_fondo(self):
        sector = self.cleaned_data['sector_fondo']
        if 'Todos' in sector:
            return [x.industria for x in rfi_bonos.objects.all().distinct('industria')]
        else:
            return sector
    def clean_payment_rank(self):
        payment_rank = self.cleaned_data['payment_rank']
        if 'Todos' in payment_rank:
            return [x.payment_rank for x in rfi_bonos.objects.all().distinct('payment_rank')]
        else:
            return payment_rank

    def clean_ytm_fondo(self):
        ytm = self.cleaned_data['ytm_fondo']
        if 'Todos' in ytm:
            return ['0 a 100','101 a 200','201 a 300','301 a 400','sobre 401']
        else:
            return ytm
    def clean_cntry_of_risk_fondo(self):
        pais = self.cleaned_data['cntry_of_risk_fondo']
        if 'Todos' in pais:
            return [x.cntry_of_risk for x in rfi_bonos.objects.all().distinct('cntry_of_risk')]
        else:
            return pais


class EditorBonos(ModelForm):
    def __init__(self,*args,**kwargs):
        super(EditorBonos,self).__init__(*args,**kwargs)
        self.fields['cusip'].widget.attrs = {'class':'form-control'}
        self.fields['security_name'].widget.attrs = {'class':'form-control'}
        self.fields['bb_composite'].widget.attrs = {'class':'form-control'}
        self.fields['payment_rank'].widget.attrs = {'class':'form-control'}
        self.fields['cntry_of_risk'].widget.attrs = {'class':'form-control'}
        self.fields['yas_mod_dur'].widget.attrs = {'class':'form-control','placeholder':'0.00'}
        self.fields['yas_bond_yld'].widget.attrs = {'class':'form-control','placeholder':'0.00'}
        self.fields['industria'].widget.attrs = {'class':'form-control'}
        self.fields['ising'].widget.attrs = {'class':'form-control'}
        
   
    class Meta:
        model = rfi_bonos
        fields = ['security_name','ising','bb_composite','payment_rank','cntry_of_risk','industria','yas_bond_yld','yas_mod_dur']
        
        
    security_name = forms.CharField(label = "Security Name del bono (*): ",required=True)
    cusip = forms.CharField(label = "Cusip del bono (*): ",required=True)
    ising = forms.CharField(label = 'Isin (*): ')
    bb_composite = forms.ChoiceField(label = "BB composite del bono (*): ",required=True,choices=listado_ratings)
    payment_rank = forms.ChoiceField(label = "Payment Rank del bono (*): ",required=True,choices=lista_paymentRank())
    cntry_of_risk = forms.ChoiceField(label = "Country of Risk del bono (*): ",required=True,choices=listado_cntry())
    industria = forms.ChoiceField(label = "Industria del bono (*): ",required=True,choices=lista_sector())
    yas_bond_yld = forms.CharField(label = "YTM del bono (*): ",required=True) #esta hay que multiplicarla por 100 -> yas_bond_porcentaje -> yas_bond_text
    yas_mod_dur = forms.CharField(label = "Duración del bono (*): ",required=True)

    def clean_yas_bond_yld(self):
        yas_bond_yld = self.cleaned_data['yas_bond_yld']
        yas_bond_yld_listo = yas_bond_yld.replace(',','.')
        return yas_bond_yld_listo
    def clean_yas_mod_dur(self):
        yas_mod_dur = self.cleaned_data['yas_mod_dur']
        yas_mod_dur_listo = yas_mod_dur.replace(',','.')
        return yas_mod_dur_listo

        
class BuscadorEditorBonosForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(BuscadorEditorBonosForm,self).__init__(*args, **kwargs)
        self.fields['isin_security_name'].choices = [(x.ising,x.ising) for x in rfi_bonos.objects.all().order_by('ising')]
       
    isin_security_name = forms.CharField()
    isin_security_name.widget.attrs = {'class':'form-control'}
    

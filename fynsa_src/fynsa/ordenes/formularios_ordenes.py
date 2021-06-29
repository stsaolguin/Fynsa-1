from django.db.models.expressions import F
from ordenes.models import rfi_tsox,fondo
from django import forms
from django.forms import ModelForm, fields
from django.forms.models import model_to_dict
from django.forms.widgets import SelectMultiple
from RFI.models import PruebaArrayModel,clientes_rfi,rfi_bonos
import datetime

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


class rfi_ingreso_orden_formulario(forms.Form):
    cliente = forms.ChoiceField(choices = [(x.fondo,x.fondo) for x in clientes_rfi.objects.all()])
    fecha_ingreso = forms.DateField(widget = forms.DateInput(attrs={'class':'form-control','type':'date'}),initial = datetime.date.today)
    orden_tipo = forms.ChoiceField(choices = [('cliente compra','cliente compra'),('cliente vende','cliente vende')])
    isin = forms.ChoiceField(choices = listado_isin(),required=False)
    papel = forms.CharField(required = False)
    rating = forms.MultipleChoiceField(choices = [('Todos','Todos'),('IG','IG'),('HY','HY')],initial='Todos',required=False)
    duracion = forms.MultipleChoiceField(choices = [('Toda la curva','Toda la curva'),('x<=3','x<=3'),('3<x<=5','3<x<=5'),('x>5','x>5')],initial='Toda la curva',required=False)
    nominales = forms.CharField(required = False)
    sector = forms.MultipleChoiceField(choices = lista_sector(),initial='Todos',required=False)
    precio = forms.CharField(required = False)
    payment_rank = forms.MultipleChoiceField(choices = lista_paymentRank(),initial='Todos',required=False)
    ytm = forms.MultipleChoiceField(choices = [('Todos','Todos'),('0 a 100','0 a 100'),('101 a 200','101 a 200'),('201 a 300','201 a 300'),('301 a 400','301 a 400'),('sobre 400','sobre 400')],initial='Todos',required=False)
    notas = forms.CharField(required = False)
    pais = forms.MultipleChoiceField(choices = listado_cntry(),initial='Todos',required=False) 

    cliente.widget.attrs.update({'class':'form-control'})
    #fecha_ingreso.widget.attrs.update({'class':'form-control'})
    orden_tipo.widget.attrs.update({'class':'form-control'})
    isin.widget.attrs.update({'class':'form-control'})
    papel.widget.attrs.update({'class':'form-control'})
    rating.widget.attrs.update({'class':'form-control'})
    duracion.widget.attrs.update({'class':'form-control'})
    nominales.widget.attrs.update({'class':'form-control'})
    sector.widget.attrs.update({'class':'form-control'})
    precio.widget.attrs.update({'class':'form-control'})
    notas.widget.attrs.update({'class':'form-control'})
    payment_rank.widget.attrs.update({'class':'form-control'})
    ytm.widget.attrs.update({'class':'form-control'})
    pais.widget.attrs.update({'class':'form-control'})

    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']
        return cliente
    
class PruebaArregloForm(ModelForm):
    class Meta:
        model = PruebaArrayModel
        fields = '__all__'


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
    cliente = forms.ChoiceField(choices = [(x.fondo,x.fondo) for x in clientes_rfi.objects.all()])
    fecha_ingreso = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}),initial = datetime.date.today)
    orden_tipo = forms.ChoiceField(choices = [('cliente compra','cliente compra'),('cliente vende','cliente vende')])
    isin = forms.ChoiceField(choices=listado_isin(),required=False)
    papel = forms.CharField(required=False)
    rating = forms.MultipleChoiceField(choices = [('Todos','Todos'),('IG','IG'),('HY','HY')],initial='Todos',required=False)
    duracion = forms.MultipleChoiceField(choices=[('Toda la curva','Toda la curva'),('x<=3','x<=3'),('3<x<=5','3<x<=5'),('x>5','x>5')],initial='Toda la curva',required=False)
    nominales = forms.CharField(required=False)
    sector = forms.MultipleChoiceField(choices=lista_sector(),initial='Todos',required=False)
    precio = forms.CharField(required=False)
    payment_rank = forms.MultipleChoiceField(choices=lista_paymentRank(),initial='Todos',required=False)
    ytm = forms.MultipleChoiceField(choices=[('Todos','Todos'),('0 a 100','0 a 100'),('101 a 200','101 a 200'),('201 a 300','201 a 300'),('301 a 400','301 a 400'),('sobre 400','sobre 400')],initial='Todos',required=False)
    notas = forms.CharField(required=False)
    pais = forms.MultipleChoiceField(choices = listado_cntry(),initial='Todos',required=False) 
    class Meta:
        model = rfi_tsox
        fields = ('cliente','fecha_ingreso','orden_tipo','nominales','precio','papel','rating','duracion','payment_rank','ytm',
        'sector','notas','pais','isin')
        
    def clean_nominales(self):
        nominales = self.cleaned_data['nominales']
        nominales = nominales.replace('.','').replace(',','.')
        return nominales

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

    nombre_fondo = forms.CharField(label="Nombre Fondo")
    duracion_fondo = forms.MultipleChoiceField(choices=[('Toda la curva','Toda la curva'),('x<=3','x<=3'),('3<x<=5','3<x<=5'),('x>5','x>5')],initial='Toda la curva',required=False)
    sector_fondo = forms.MultipleChoiceField(choices=lista_sector(),initial='Todos',required=False)
    ytm_fondo = forms.MultipleChoiceField(choices=[('Todos','Todos'),('0 a 100','0 a 100'),('101 a 200','101 a 200'),('201 a 300','201 a 300'),('301 a 400','301 a 400'),('sobre 400','sobre 400')],initial='Todos',required=False)
    risk_fondo = forms.MultipleChoiceField(choices = [('Todos','Todos'),('IG','IG'),('HY','HY')],initial='Todos',required=False)
    cntry_of_risk_fondo = forms.MultipleChoiceField(choices = listado_cntry(),initial='Todos',required=False) 
    trader_fondo = forms.CharField(required=False)
    tamano_fondo = forms.CharField(label='Tamaño del fondo (en Millones).',required=False)
    notas_fondo = forms.CharField(required=False)

    class Meta:
        model = fondo
        fields = '__all__'
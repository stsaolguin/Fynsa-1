from django.forms import ModelForm, Textarea,Select,DateInput, ModelChoiceField
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxInput
from django.utils import tree
from .models import *
from django import forms
from RFI.models import rfi_beta
from datetime import datetime

def ultima_fecha_bases():
    bases.refresh_from_db
    a = bases.objects.latest('fecha').fecha
    return str(a)

def ultima_fecha_rfi():
    rfi_beta.refresh_from_db
    return str(rfi_beta.objects.latest('fecha').fecha)
    

def clientes_conciliaciones():
    """ esta funcion es para las conciliaciones """
    return clientes.objects.filter(factura=True).order_by('nombre')

def clientes_total():
    return clientes.objects.filter(factura=True).values_list('nombre','nombre')

class f_bases(ModelForm):
    class Meta:
        model= bases
        fields = '__all__'
        widgets = {
            'nemo':Textarea(attrs={'class':'form-control'}),
            'dias':DateInput(attrs={'class':'form-control'}),
            'buy':Select(attrs={'class':'form-control'}),
            'seller':Select(attrs={'class':'form-control'}),
            'monto':Textarea(attrs={'class':'form-control'}),
            'trader_buy':Select(attrs={'class':'form-control'}),
            'trader_seller':Select(attrs={'class':'form-control'}),
            'fee_buyer_clp':Textarea(attrs={'class':'form-control'}),
            'fee_seller_clp':Textarea(attrs={'class':'form-control'}),
            'participante_1':Select(attrs={'class':'form-control'}),
            'participante_2':Select(attrs={'class':'form-control'}),

        }
    

class f_fechas_comite(forms.Form):
    def __init__(self,*args,**kwarg):
        super(f_fechas_comite,self).__init__(*args,**kwarg)
        self.fields['fecha_final'].initial=ultima_fecha_bases()
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True)

class f_fechas_comite_rfi(forms.Form):
    def __init__(self,*args,**kwarg):
        super(f_fechas_comite_rfi,self).__init__(*args,**kwarg)
        self.fields['fecha_final'].initial=ultima_fecha_rfi()
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Inicial', required=True, initial='2021-01-01')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Final', required=True)

class f_conciliaciones(forms.Form):
    def __init__(self,*args,**kwarg):
        super(f_conciliaciones,self).__init__(*args,**kwarg)
        self.fields['fecha_final'].initial=ultima_fecha_bases()
    cliente = forms.ModelChoiceField(queryset=clientes_conciliaciones(),to_field_name='nombre')
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True)
    en_dolares = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control mx-2','type':'checkbox'}),required = False)
    cliente.widget.attrs.update({'class':'form-control mx-2'})


#clientes=clientes.objects.filter(factura=True).values_list('nombre','nombre')


class f_facturas_bases(ModelForm):
    model=facturas_bases
    class Meta:
        widgets ={
            'cliente' : Select(choices=clientes_total())
        }

class bases_ingreso_operaciones(ModelForm):
    class Meta:
        clientes = [(x.institucion_trader,x.institucion_trader) for x in cliente_trader.objects.all().order_by('institucion_trader')] 
        instrumentos = [(x.nemo,x.nemo) for x in bases.objects.filter(nemo__startswith='B').distinct('nemo').order_by('-nemo')]
        model = bases
        fields = ['fecha','nemo','tipo_de_pago','otc_tr','fynsa','buy','seller','fee_buyer_clp','fee_seller_clp','monto','compra_depo','venta_depo','tasa_buyer','tasa_seller']
        widgets = {
            'nemo': forms.Select(attrs={'class': "form-control"},choices = instrumentos),
            'buy': forms.Select(attrs={'class': "form-control"},choices = clientes),
            'seller': forms.Select(attrs={'class': "form-control"},choices = clientes),
            'fynsa': forms.Select(attrs={'class': "form-control"}),
            'otc_tr': forms.Select(attrs={'class': "form-control"}),
            'monto' : forms.TextInput(attrs={'class': "form-control","placeholder":"0"}),
            'tasa_buyer' : forms.TextInput(attrs={'class': "form-control"}),
            'tasa_seller' : forms.TextInput(attrs={'class': "form-control"}),
            'compra_depo' : forms.TextInput(attrs={'class': "form-control"}),
            'venta_depo' : forms.TextInput(attrs={'class': "form-control"}),
            'fecha' : forms.DateInput(attrs={'class': "form-control",'type':'date'}),
            'tipo_de_pago' : forms.Select(attrs={'class': "form-control"}),
            'fee_buyer_clp' : forms.TextInput(attrs={'class': "form-control"}),
            'fee_seller_clp' : forms.TextInput(attrs={'class': "form-control"}),
            'dias' : forms.NumberInput(attrs={'class': "form-control"}),
        }
    def clean(self):
        super().clean()
        vendedor = self.cleaned_data.get("seller")
        comprador = self.cleaned_data.get("buy")
        monto_comprador = self.cleaned_data.get("compra_depo")
        monto_vendedor = self.cleaned_data.get("venta_depo")
        lista_de_errores = []
        if comprador==vendedor:
            lista_de_errores.append(ValidationError("vendedor y comprador no pueden ser el mismo, Ojo ahí!"))
        if len(lista_de_errores)>0:
            raise ValidationError(lista_de_errores)
        
    


class cargador_bases_form(forms.Form):
    bases = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))

class cargador_bases_form2(forms.Form):
    ruta = forms.FileField(
        label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",
        widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3','multiple':True})) # el multiple true asegura que puedes subir muchos archivos

class cargador_rfi_form(forms.Form):
    rfi = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))

class bases_ingreso_operaciones_depos(ModelForm):
    class Meta:
        clientes = [(x.institucion_trader,x.institucion_trader) for x in cliente_trader.objects.all().order_by('institucion_trader')] 
        instrumentos = [(x.nemo,x.nemo) for x in bases.objects.filter(nemo__startswith='F').distinct('nemo').order_by('-nemo')]
        model = bases
        fields = ['fecha','nemo','tipo_de_pago','otc_tr','fynsa','buy','seller','fee_buyer_clp','fee_seller_clp','monto','compra_depo','venta_depo','tasa_buyer','tasa_seller','dias']
        widgets = {
                'nemo': forms.Select(attrs={'class': "form-control",'id':'id_nemo_depositos'},choices = instrumentos),
                'buy': forms.Select(attrs={'class': "form-control",'id':'id_buy_depositos'},choices = clientes),
                'seller': forms.Select(attrs={'class': "form-control",'id':'id_seller_depositos'},choices = clientes),
                'fynsa': forms.Select(attrs={'class': "form-control",'id':'id_fynsa_depositos'}),
                'otc_tr': forms.Select(attrs={'class': "form-control",'id':'id_otc_tr_depositos'}),
                'monto' : forms.TextInput(attrs={'class': "form-control","placeholder":"0",'id':'id_monto_depositos'}),
                'tasa_buyer' : forms.TextInput(attrs={'class': "form-control",'id':'id_tasa_buyer_depositos'}),
                'tasa_seller' : forms.TextInput(attrs={'class': "form-control",'id':'id_tasa_seller_depositos'}),
                'compra_depo' : forms.TextInput(attrs={'class': "form-control",'id':'id_compra_depositos'}),
                'venta_depo' : forms.TextInput(attrs={'class': "form-control",'id':'id_venta_depositos'}),
                'fecha' : forms.DateInput(attrs={'class': "form-control",'type':'date','id':'id_fecha_depositos'}),
                'tipo_de_pago' : forms.Select(attrs={'class': "form-control",'id':'id_tipo_de_pago_depositos'}),
                'fee_buyer_clp' : forms.TextInput(attrs={'class': "form-control",'id':'id_fee_buyer_depositos'}),
                'fee_seller_clp' : forms.TextInput(attrs={'class': "form-control",'id':'id_fee_seller_depositos'}),
                'dias' : forms.NumberInput(attrs={'class': "form-control",'id':'id_dias_depositos'})
                }
    def clean(self):
        super().clean()
        vendedor = self.cleaned_data.get("seller")
        comprador = self.cleaned_data.get("buy")
        monto_comprador = self.cleaned_data.get("compra_depo")
        monto_vendedor = self.cleaned_data.get("venta_depo")
        lista_de_errores = []
        if comprador==vendedor:
            lista_de_errores.append(ValidationError("vendedor y comprador no pueden ser el mismo, Ojo ahí!"))
        if len(lista_de_errores)>0:
            raise ValidationError(lista_de_errores)


class BlotterModelForm(forms.ModelForm):
    class Meta:
        model = bases
        exclude=[
        'concate', 
    'institucion_trader_buyer', 
    'institucion_trader_seller',
    'institucion_trader_participante_1',
    'institucion_trader_participante_2', 
    'tasa_buyer',
    'tasa_seller',
    'tipo_de_cambio',
    'uf',
    ]
        

    def clean_participante_1(self):
        return self.cleaned_data['participante_1'] or None
    def clean_participante_2(self):
        return self.cleaned_data['participante_2'] or None
    def clean_institucion_trader_participante_1(self):
        return self.cleaned_data['institucion_trader_participante_1'] or None
    def clean_institucion_trader_participante_2(self):
        return self.cleaned_data['institucion_trader_participante_1'] or None
 
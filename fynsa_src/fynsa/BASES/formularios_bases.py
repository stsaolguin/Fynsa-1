from django.forms import ModelForm, Textarea,Select,DateInput, ModelChoiceField
from .models import *
from django import forms
from RFI.models import rfi_beta


ultima_fecha = bases.objects.latest('fecha')
ultima_fecha_rfi = rfi_beta.objects.latest('fecha')
ultima_fecha.refresh_from_db()
ultima_fecha_rfi.refresh_from_db()

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
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True, initial=ultima_fecha)

class f_fechas_comite_rfi(forms.Form):
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Inicial', required=True, initial='2021-01-01')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Final', required=True, initial=rfi_beta.objects.latest('fecha'))

class f_conciliaciones(forms.Form):
    cliente = forms.ModelChoiceField(queryset=clientes.objects.filter(factura=True).order_by('nombre'),to_field_name='nombre')
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True, initial=ultima_fecha)
    cliente.widget.attrs.update({'class':'form-control mx-2'})


clientes=clientes.objects.filter(factura=True).values_list('nombre','nombre')


class f_facturas_bases(ModelForm):
    model=facturas_bases
    class Meta:
        #cliente
        widgets ={
            'cliente' : Select(choices=clientes)
        }

class bases_ingreso_operaciones(ModelForm):
    class Meta:
        clientes = [(x.institucion_trader,x.institucion_trader) for x in cliente_trader.objects.all().order_by('-institucion_trader')] 
        instrumentos = [(x.nemo,x.nemo) for x in bases.objects.distinct('nemo').order_by('-nemo')]
        model = bases
        fields = ['fecha','nemo','tipo_de_pago','otc_tr','fynsa','buy','seller','fee_buyer_clp','fee_seller_clp','monto','tasa','valor_final','compra_depo','venta_depo','tasa_buyer','tasa_seller']
        widgets = {
            'nemo': forms.Select(attrs={'class': "form-control"},choices = instrumentos),
            'buy': forms.Select(attrs={'class': "form-control"},choices = clientes),
            'seller': forms.Select(attrs={'class': "form-control"},choices = clientes),
            'fynsa': forms.Select(attrs={'class': "form-control"},choices = ['SI','NO']),
            'otc_tr': forms.Select(attrs={'class': "form-control"},choices = ['OTC','TR']),
            'monto' : forms.TextInput(attrs={'class': "form-control","placeholder":"0"}),
            'tasa_buyer' : forms.TextInput(attrs={'class': "form-control"}),
            'tasa_seller' : forms.TextInput(attrs={'class': "form-control"}),
            'compra_depo' : forms.TextInput(attrs={'class': "form-control"}),
            'venta_depo' : forms.TextInput(attrs={'class': "form-control"}),
            'fecha' : forms.DateInput(attrs={'class': "form-control",'type':'date'}),
            'tipo_de_pago' : forms.Select(attrs={'class': "form-control"},choices=[('PH','PH'),('PM','PM'),('CN','CN')]),
            'fee_buyer_clp' : forms.TextInput(attrs={'class': "form-control"}),
            'fee_seller_clp' : forms.TextInput(attrs={'class': "form-control"}),
        }
    
    


class cargador_bases_form(forms.Form):
    bases = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))

class cargador_rfi_form(forms.Form):
    rfi = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))

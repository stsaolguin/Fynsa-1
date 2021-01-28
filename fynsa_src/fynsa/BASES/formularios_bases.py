from django.forms import ModelForm, Textarea,Select,DateInput, ModelChoiceField
from .models import *
from django import forms
from RFI.models import rfi_beta


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
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True, initial=bases.objects.latest('fecha'))

class f_fechas_comite_rfi(forms.Form):
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Inicial', required=True, initial='2021-01-01')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Final', required=True, initial=rfi_beta.objects.latest('fecha'))

class f_conciliaciones(forms.Form):
    cliente = forms.ModelChoiceField(queryset=clientes.objects.filter(factura=True).order_by('nombre'),to_field_name='nombre')
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True, initial=bases.objects.latest('fecha'))
    cliente.widget.attrs.update({'class':'form-control mx-2'})


clientes=clientes.objects.filter(factura=True).values_list('nombre','nombre')


class f_facturas_bases(ModelForm):
    model=facturas_bases
    class Meta:
        #cliente
        widgets ={
            'cliente' : Select(choices=clientes)
        }
        
        
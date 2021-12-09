from django import forms
from django.contrib.postgres import fields
from RFI.models import rfi_beta
from ordenes.formularios_ordenes import dia_actual



class cargador_rfi_beta_form(forms.Form):
    rfi_beta = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))


class IngresoOperacionesRfiBeta(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(IngresoOperacionesRfiBeta,self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs = {'class':'form-control'}
        self.fields['papel'].widget.attrs = {'class':'form-control'}
        self.fields['cusip'].widget.attrs = {'class':'form-control'}
        self.fields['operacion'].widget.attrs = {'class':'form-control'}
        self.fields['nominales'].widget.attrs = {'class':'form-control'}
        self.fields['mesa'].widget.attrs = {'class':'form-control'}
        self.fields['ejecutivo_precio'].widget.attrs = {'class':'form-control'}
        self.fields['cliente_precio'].widget.attrs = {'class':'form-control'}
        self.fields['ingreso_ejecutivo'].widget.attrs = {'class':'form-control'}
        self.fields['ingreso_mesa'].widget.attrs = {'class':'form-control'}
        self.fields['contraparte'].widget.attrs = {'class':'form-control'}
        self.fields['spread_mesa'].widget.attrs = {'class':'form-control'}
        self.fields['comprador'].widget.attrs = {'class':'form-control'}
        self.fields['vendedor'].widget.attrs = {'class':'form-control'}
        self.fields['country_of_risk'].widget.attrs = {'class':'form-control'}
        self.fields['crncy'].widget.attrs = {'class':'form-control'}
        
    class Meta:
        model = rfi_beta
        exclude =['linea','tipo_de_cambio','fecha_subido','duration','ejecutivo','cliente']
    fecha = forms.DateField(widget = forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type':'date'}),initial = dia_actual())
    papel = forms.CharField(required = True)
    cusip = forms.CharField(required = True)
    nominales = forms.CharField(required = True, initial = 0)
    mesa = forms.CharField(required = True, initial = 0)
    ejecutivo_precio = forms.CharField(required = True,initial = 0)
    cliente_precio = forms.CharField(required = True)
    ingreso_ejecutivo = forms.CharField(required = True)
    spread_mesa = forms.CharField(disabled = True,initial = 0)
    ingreso_mesa = forms.CharField(disabled = True,initial = 0)
    comprador = forms.ChoiceField(required = True)
    vendedor = forms.ChoiceField(required = True)

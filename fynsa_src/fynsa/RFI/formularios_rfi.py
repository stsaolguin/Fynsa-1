from django import forms
from django.contrib.postgres import fields
from RFI.models import rfi_beta,clientes_rfi,ejecutivos_externos_bp
from ordenes.formularios_ordenes import dia_actual,listado_isin
from RFI.funcion_truncar import truncar

def clientes_rfi_iterable():
    c = clientes_rfi.objects.all().order_by('fondo')
    return [(x.fondo,x.fondo) for x in c]

def cliente_rfi_iterable():
    """Esta función trae el iterable para las cuentas tipo PIU00239"""
    c = rfi_beta.objects.distinct('cliente').order_by('cliente')
    return [(x.cliente,x.cliente) for x in c]

def ejecutivos_bp_iterable():
    """Obtiene el nombre de los ejecutivos"""
    d = ejecutivos_externos_bp.objects.all()
    return [(x.nombre_completo,x.nombre_completo) for x in d]

class cargador_rfi_beta_form(forms.Form):
    rfi_beta = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))


class IngresoOperacionesRfiBetaIntermediacion(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(IngresoOperacionesRfiBetaIntermediacion,self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs = {'class':'form-control'}
        self.fields['papel'].widget.attrs = {'class':'form-control','readonly':'readonly'}
        self.fields['cusip'].widget.attrs = {'class':'form-control'}
        self.fields['nominales'].widget.attrs = {'class':'form-control'}
        self.fields['mesa'].widget.attrs = {'class':'form-control'}
        self.fields['ejecutivo_precio'].widget.attrs = {'class':'form-control'}
        #self.fields['ingreso_ejecutivo'].widget.attrs = {'class':'form-control','readonly':'readonly'}
        self.fields['ingreso_mesa'].widget.attrs = {'class':'form-control','readonly':'readonly'}
        #self.fields['contraparte'].widget.attrs = {'class':'form-control'}
        self.fields['spread_mesa'].widget.attrs = {'class':'form-control','readonly':'readonly'}
        self.fields['comprador'].widget.attrs = {'class':'form-control'}
        self.fields['vendedor'].widget.attrs = {'class':'form-control'}
        self.fields['country_of_risk'].widget.attrs = {'class':'form-control'}
        self.fields['crncy'].widget.attrs = {'class':'form-control'}
        self.fields['comprador'].choices = clientes_rfi_iterable()
        self.fields['vendedor'].choices = clientes_rfi_iterable()
        self.fields['cusip'].choices = listado_isin()
        
    class Meta:
        model = rfi_beta
        exclude =['linea','tipo_de_cambio','fecha_subido','duration','ejecutivo','cliente','operacion','ingreso_ejecutivo','contraparte','cliente_precio']
    fecha = forms.DateField(widget = forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type':'date'}),initial = dia_actual())
    papel = forms.CharField(required = True)
    cusip = forms.CharField(required = True)
    nominales = forms.CharField(required = True, initial = 0)
    mesa = forms.CharField(required = True, initial = 0)
    ejecutivo_precio = forms.CharField(required = True,initial = 0)
    spread_mesa = forms.CharField(initial = 0)
    ingreso_mesa = forms.CharField(initial = 0)
    comprador = forms.ChoiceField(required = True)
    vendedor = forms.ChoiceField(required = True)

    def clean_nominales(self):
        nominales = self.cleaned_data['nominales']
        return nominales.replace('.','')
    def clean_ingreso_mesa(self):
        ingreso_mesa = self.cleaned_data['ingreso_mesa']
        return truncar(ingreso_mesa,2)
    def clean_spread_mesa(self):
        spread_mesa = self.cleaned_data['spread_mesa']
        return truncar(spread_mesa,3)

class IngresoOperacionesRfiBetaCruceInterno(IngresoOperacionesRfiBetaIntermediacion):
    def __init__(self,*args, **kwargs):
        super(IngresoOperacionesRfiBetaCruceInterno,self).__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs = {'class':'form-control'}
        self.fields['cliente'].choices = cliente_rfi_iterable()
        self.fields['ejecutivo'].widget.attrs = {'class':'form-control'}
        self.fields['ejecutivo'].choices = ejecutivos_bp_iterable()
        self.fields['cliente_precio'].widget.attrs = {'class':'form-control'}
        
    
    cliente = forms.ChoiceField(required = True)
    ejecutivo = forms.ChoiceField(required = True)
    cliente_precio = forms.CharField(required = True)
    prefix = "cruce"
    


class IngresoOperacionesRfiBetaCompraVentaEjecutivos(IngresoOperacionesRfiBetaCruceInterno):
    prefix="compraventa"
    
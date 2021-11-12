from django import forms
from django.contrib.postgres import fields
from RFI.models import rfi_beta



class cargador_rfi_beta_form(forms.Form):
    rfi_beta = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))


class IngresoOperacionesRfiBeta(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(IngresoOperacionesRfiBeta,self).__init__(*args, **kwargs)
        pass
    class Meta:
        model = rfi_beta
        fields = '__all__'
        

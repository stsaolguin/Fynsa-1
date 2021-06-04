from django import forms
from django.forms import ModelForm, fields
from django.forms.widgets import SelectMultiple
from RFI.models import PruebaArrayModel,clientes_rfi,rfi_bonos
import datetime




class rfi_ingreso_orden_formulario(forms.Form):
    cliente = forms.ChoiceField(choices = [(x.fondo,x.fondo) for x in clientes_rfi.objects.all()])
    fecha = forms.DateField(initial = datetime.date.today)
    orden = forms.ChoiceField(choices = [('cliente compra','cliente compra'),('cliente vende','cliente vende')])
    isin = forms.CharField()
    papel = forms.CharField()
    rating = forms.MultipleChoiceField(choices = [('IG','IG'),('HY','HY')])
    duration_text = forms.ChoiceField(choices=[(x.dur_text,x.dur_text) for x in rfi_bonos.objects.all().distinct('dur_text')])
    nominales = forms.CharField()
    sector = forms.MultipleChoiceField(choices=[(x.classification,x.classification) for x in rfi_bonos.objects.all().distinct('industria')])
    precio = forms.CharField()
    payment_rank = forms.MultipleChoiceField(choices=[(x.payment_rank,x.payment_rank) for x in rfi_bonos.objects.all().distinct('payment_rank')])
    notas = forms.CharField(max_length=100)

    cliente.widget.attrs.update({'class':'form-control'})
    fecha.widget.attrs.update({'class':'form-control'})
    orden.widget.attrs.update({'class':'form-control'})
    isin.widget.attrs.update({'class':'form-control'})
    papel.widget.attrs.update({'class':'form-control'})
    rating.widget.attrs.update({'class':'form-control'})
    duration_text.widget.attrs.update({'class':'form-control'})
    nominales.widget.attrs.update({'class':'form-control'})
    sector.widget.attrs.update({'class':'form-control'})
    precio.widget.attrs.update({'class':'form-control'})
    notas.widget.attrs.update({'class':'form-control'})
    payment_rank.widget.attrs.update({'class':'form-control'})


    
class PruebaArregloForm(ModelForm):
    class Meta:
        model = PruebaArrayModel
        fields = '__all__'

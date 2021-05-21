from django import forms


class rfi_ingreso_orden_formulario(forms.Form):
    cliente = forms.ChoiceField(choices=[('cliente1','cliente1'),('cliente2','cliente2'),('cliente3','cliente3')])
    fecha = forms.DateTimeField()
    orden = forms.ChoiceField(choices=[('cliente compra','cliente compra'),('cliente vende','cliente vende')])
    isin = forms.CharField()
    papel = forms.CharField()
    rating = forms.CharField()
    duration_text = forms.CharField()
    nominales = forms.CharField()
    sector = forms.CharField()
    precio = forms.CharField()

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


    

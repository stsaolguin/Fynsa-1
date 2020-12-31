from django import forms

class lva_1(forms.Form):
    tr = forms.FileField(label="Archivo Telerenta (formato RRES)",widget=forms.FileInput(attrs={'class':'form-control'}))
    rsk = forms.FileField(label="Archivo Riskamérica (formato RESUME)",widget=forms.FileInput(attrs={'class':'form-control'}))



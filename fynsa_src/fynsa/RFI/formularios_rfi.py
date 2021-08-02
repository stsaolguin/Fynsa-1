from django import forms



class cargador_rfi_beta_form(forms.Form):
    rfi_beta = forms.FileField(label="Archivo del blotter, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))




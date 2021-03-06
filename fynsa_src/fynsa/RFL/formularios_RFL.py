from django import forms
from RFL.models import archivos_cintas
from django.core.exceptions import ValidationError
import csv,io

class lva_1_2(forms.Form):
    tr = forms.FileField(label="Archivo Telerenta (formato RRES), UTF-8 separado por punto y coma",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))
    rsk = forms.FileField(label="Archivo Riskamérica (formato RESUME), UTF-8 separado por punto y coma",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))
    #validar si los archivos son csv utf8 y tienen los campos correctos

categorias=[
    ('BB','Bonos Bancarios'),
    ('BE','Bonos Empresa'),
    ('BU','Bonos Subordinados'),
    ('BS','Bonos Securitizados')
    ]
moneda = [('UF','UF'),('CLP','CLP')]
rating = [('AAA','AAA'),('AA+','AA+'),('AA','AA'),('AA-','AA-'),('A+','A+'),('A','A'),('A-','A-'),('BBB+','BBB+'),('BBB','BBB'),('BBB-','BBB-'),('BB+','BB+'),('BB','BB'),('BB-','BB-')]
atributo =({'class':'form-control mx-3 my-2'})

class formulario_consulta_cintas(forms.Form):
    categoria = forms.ChoiceField(choices=categorias,widget=forms.Select(attrs=atributo))
    rating = forms.ChoiceField(choices=rating,widget=forms.Select(attrs=atributo))
    moneda = forms.ChoiceField(choices=moneda,widget=forms.Select(attrs=atributo))
    duracion_inicial = forms.DecimalField(label="Duración inicial (000.00)",min_value=0,max_value=999.99,max_digits=5, decimal_places=2,widget=forms.NumberInput(attrs=atributo))
    duracion_final = forms.DecimalField(label="Duración final (000.00)",min_value=0,max_value=999.99,max_digits=5, decimal_places=2,widget=forms.NumberInput(attrs=atributo))

    
class formulario_posiciones(forms.Form):
    pos = forms.FileField(label="Archivo Posiciones institucionales, UTF-8 separado por punto y coma",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))

class formulario_lva(forms.Form):
    lva = forms.FileField(label="Archivo LVA, UTF-8 separado por punto y coma (CSV UTF-8)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))
    
class formulario_consulta_supercintas(forms.Form):
    categoria = forms.ChoiceField(choices=categorias,widget=forms.Select(attrs=atributo))
    rating = forms.ChoiceField(choices=rating,widget=forms.Select(attrs=atributo))
    moneda = forms.ChoiceField(choices=moneda,widget=forms.Select(attrs=atributo))
    duracion_inicial = forms.DecimalField(label="Duración inicial (000.00)",min_value=0,max_value=999.99,max_digits=5, decimal_places=2,widget=forms.NumberInput(attrs=atributo))
    duracion_final = forms.DecimalField(label="Duración final (000.00)",min_value=0,max_value=999.99,max_digits=5, decimal_places=2,widget=forms.NumberInput(attrs=atributo))
    
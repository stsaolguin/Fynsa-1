from django import forms

class lva_1(forms.Form):
    tr = forms.FileField(label="Archivo Telerenta (formato RRES)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))
    rsk = forms.FileField(label="Archivo Riskamérica (formato RESUME)",widget=forms.FileInput(attrs={'class':'form-control mx-2 my-3'}))


categorias=[
    ('BB','Bonos Bancarios'),
    ('BE','Bonos Empresa'),
    ('BU','Bonos Subordinaods'),
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



from django.forms import ModelForm, Textarea,Select,DateInput, ModelChoiceField
from .models import *
from django import forms
from RFI.models import rfi_beta


clientes_bases=[("VISION","VISION"),
("TELERENTA","TELERENTA"),
("FYNSA","FYNSA"),
("FM SURA","FM SURA"),
("FM SECURITY","FM SECURITY"),
("FM SCOTIABANK","FM SCOTIABANK"),
("FM ITAU","FM ITAU"),
("FM FYNSA","FM FYNSA"),
("FM BCI","FM BCI"),
("CDS PRINCIPAL","CDS PRINCIPAL"),
("CDS EUROAMERICA","CDS EUROAMERICA"),
("CDS BICE","CDS BICE"),
("CB CREDICORP","CB CREDICORP"),
("CB CONSORCIO","CB CONSORCIO"),
("CB BTG","CB BTG"),
("CB BCI","CB BCI"),
("B SECURITY","B SECURITY"),
("B SCOTIABANK","B SCOTIABANK"),
("B SANTANDER","B SANTANDER"),
("B JPM","B JPM"),
("B HSBC","B HSBC"),
("B FALABELLA","B FALABELLA"),
("B ESTADO","B ESTADO"),
("B CONSORCIO","B CONSORCIO"),
("BCONSORCIO","BCONSORCIO"),
("B CHILE","B CHILE"),
("B BTG","B BTG"),
("B BICE","B BICE"),
("B BCI","B BCI"),
("AFP PLANVITAL","AFP PLANVITAL"),
("AFP MODELO","AFP MODELO"),
("AFP HABITAT","AFP HABITAT"),
("AFP CAPITAL","AFP CAPITAL"),
("AFP AFC","AFP AFC"),
("BANCHILE","BANCHILE"),
("B ITAU","B ITAU"),
("B INTERNACIONAL","B INTERNACIONAL"),
("B MERRIL LYNCH","B MERRIL LYNCH"),
("FM BANCHILE","FM BANCHILE"),
("CB EUROAMERICA","CB EUROAMERICA"),
("FM CREDICORP","FM CREDICORP"),
("FM BTG","FM BTG"),
("FM SCOTIA","FM SCOTIA"),
("FM SANTANDER","FM SANTANDER"),
("FM MONEDA","FM MONEDA"),
("FM LARRAIN VIAL","FM LARRAIN VIAL"),
("HSBC","HSBC"),

]

traders=[
    ("ALAIN JELVEZ","ALAIN JELVEZ"),
("ALDO FERRARI","ALDO FERRARI"),
("ALEXIS VEGA","ALEXIS VEGA"),
("ALVARO MARIN","ALVARO MARIN"),
("CARLOS FEMENIAS","CARLOS FEMENIAS"),
("CATALINA MONCADA","CATALINA MONCADA"),
("CHRISTIAN GOMEZ","CHRISTIAN GOMEZ"),
("CLAUDIO RICKE","CLAUDIO RICKE"),
("CRISTIAN CATALDO","CRISTIAN CATALDO"),
("CRISTIAN FUENTES","CRISTIAN FUENTES"),
("CRISTIAN GOMEZ","CRISTIAN GOMEZ"),
("CRISTIAN MORENO","CRISTIAN MORENO"),
("CRISTIAN SEPULVEDA","CRISTIAN SEPULVEDA"),
("CRISTOBAL RIOS","CRISTOBAL RIOS"),
("CRISTOBAL ROSAS","CRISTOBAL ROSAS"),
("DIEGO SOUPER","DIEGO SOUPER"),
("EDUARDO SANTANA","EDUARDO SANTANA"),
("ELIAS PICHARA","ELIAS PICHARA"),
("EUGENIO ZAMORANO","EUGENIO ZAMORANO"),
("FEDERICO ALONSO","FEDERICO ALONSO"),
("FELIPE LOZANO","FELIPE LOZANO"),
("FELIPE MENA","FELIPE MENA"),
("FYNSA","FYNSA"),
("GABRIELA VANZULLI","GABRIELA VANZULLI"),
("GABRIELA VARGAS","GABRIELA VARGAS"),
("GONZALO JIMENEZ","GONZALO JIMENEZ"),
("GONZALO MARTINEZ","GONZALO MARTINEZ"),
("GONZALO MONCADA","GONZALO MONCADA"),
("GUSTAVO FUENTEALBA","GUSTAVO FUENTEALBA"),
("IGNACIO SILVA","IGNACIO SILVA"),
("JAVIER VALENCIA","JAVIER VALENCIA"),
("JOAQUIN CORTEZ","JOAQUIN CORTEZ"),
("JOAQUIN GOMEZ","JOAQUIN GOMEZ"),
("JOAQUIN SPORKE","JOAQUIN SPORKE"),
("JORGE SANCHEZ","JORGE SANCHEZ"),
("JORGE TROMBERG","JORGE TROMBERG"),
("JORGE TROMBERT","JORGE TROMBERT"),
("JOSE AGUSTIN CRISTI","JOSE AGUSTIN CRISTI"),
("JOSE LABRAÑA","JOSE LABRAÑA"),
("JOSE MIGUEL GREDILLA","JOSE MIGUEL GREDILLA"),
("JPM","JPM"),
("JUAN ANDRES MORA","JUAN ANDRES MORA"),
("JUAN GAJARDO","JUAN GAJARDO"),
("JUAN GUAJARDO","JUAN GUAJARDO"),
("JUAN MANUEL BECAR","JUAN MANUEL BECAR"),
("LARRY VIDAL","LARRY VIDAL"),
("MAGDALENA CASANOVA","MAGDALENA CASANOVA"),
("MARCELA TEJADA","MARCELA TEJADA"),
("MARCELO ZARATE","MARCELO ZARATE"),
("MATIAS CORTES","MATIAS CORTES"),
("MATIAS ROJAS","MATIAS ROJAS"),
("MATIAS TORRES","MATIAS TORRES"),
("MAX BUSCH","MAX BUSCH"),
("MIGUEL SARMIENTO","MIGUEL SARMIENTO"),
("NAHIM FARAH","NAHIM FARAH"),
("PABLO ARROYO","PABLO ARROYO"),
("PABLO COLOMA","PABLO COLOMA"),
("PABLO ORMAZABAL","PABLO ORMAZABAL"),
("PABLO ZAGAL","PABLO ZAGAL"),
("PATRICIO PEÑA Y LILLO","PATRICIO PEÑA Y LILLO"),
("PATRICIO SALDAÑA","PATRICIO SALDAÑA"),
("PATRICIO SEPULVEDA","PATRICIO SEPULVEDA"),
("RODRIGO SEPULVEDA","RODRIGO SEPULVEDA"),
("RODRIGO YAÑEZ","RODRIGO YAÑEZ"),
("SEBASTIAN MORALES","SEBASTIAN MORALES"),
("STEFAN ZEAGUEL","STEFAN ZEAGUEL"),
("TELERENTA","TELERENTA"),
("TOMAS SILVA","TOMAS SILVA"),
("VICTOR VALENZUELA","VICTOR VALENZUELA"),
("ADOLFO HORMAZABAL","ADOLFO HORMAZABAL"),
("ALEX JARA","ALEX JARA"),
("ALVARO DARQUEA","ALVARO DARQUEA"),
("ANDRES PRICE","ANDRES PRICE"),
("AYLI FUENTES","AYLI FUENTES"),
("BENAJMIN GUEVARA","BENAJMIN GUEVARA"),
("BERNARNO HASENLECHNER","BERNARNO HASENLECHNER"),
("CAMILA TOMBOLINI","CAMILA TOMBOLINI"),
("CAROLINA RUIZ","CAROLINA RUIZ"),
("CHRISTIAN AHUMADA","CHRISTIAN AHUMADA"),
("CLAUDIO TAPIA","CLAUDIO TAPIA"),
("CRISTIAN ALAMOS","CRISTIAN ALAMOS"),
("DANIEL ARANGUIZ","DANIEL ARANGUIZ"),
("DANTON QUEZADA","DANTON QUEZADA"),
("ERICH KAEMPFE","ERICH KAEMPFE"),
("GONZALO SILVA","GONZALO SILVA"),
("GUILLERMO HARRIS","GUILLERMO HARRIS"),
("HECTOR CANALES","HECTOR CANALES"),
("IGNACIO RIVEROS","IGNACIO RIVEROS"),
("IVAN ALVAREZ","IVAN ALVAREZ"),
("JAIME GAJARDO","JAIME GAJARDO"),
("JAVIER URZUA","JAVIER URZUA"),
("JUAN IGNACIO DE VICENTE","JUAN IGNACIO DE VICENTE"),
("KEITH WATT","KEITH WATT"),
("LUIS PEREZ","LUIS PEREZ"),
("MANUEL GONZALEZ","MANUEL GONZALEZ"),
("NICOLAS VALDERRAMA","NICOLAS VALDERRAMA"),
("PABLO UMAÑA","PABLO UMAÑA"),
("PAULINA ALCALDE","PAULINA ALCALDE"),
("RICARDO ARRATIA","RICARDO ARRATIA"),
("RODRIGO ARTECHE","RODRIGO ARTECHE"),
("STEFAN ZIEGUEL","STEFAN ZIEGUEL"),

]



class f_bases(ModelForm):
    class Meta:
        model= bases
        fields = '__all__'
        widgets = {
            'nemo':Textarea(attrs={'class':'form-control'}),
            'dias':DateInput(attrs={'class':'form-control'}),
            'buy':Select(attrs={'class':'form-control'},choices=clientes_bases),
            'seller':Select(attrs={'class':'form-control'},choices=clientes_bases),
            'monto':Textarea(attrs={'class':'form-control'}),
            'trader_buy':Select(attrs={'class':'form-control'},choices=traders),
            'trader_seller':Select(attrs={'class':'form-control'},choices=traders),
            'fee_buyer_clp':Textarea(attrs={'class':'form-control'}),
            'fee_seller_clp':Textarea(attrs={'class':'form-control'}),
            'participante_1':Select(attrs={'class':'form-control'},choices=clientes_bases),
            'participante_2':Select(attrs={'class':'form-control'},choices=clientes_bases),

        }
    

class f_fechas_comite(forms.Form):
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha inicial', required=True, initial='2019-08-09')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='fecha final', required=True, initial=bases.objects.latest('fecha'))

class f_fechas_comite_rfi(forms.Form):
    fecha_inicial = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Inicial', required=True, initial='2020-01-01')
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mx-2','type':'date'}),label='Fecha Final', required=True, initial=rfi_beta.objects.latest('fecha'))

class f_conciliaciones(forms.Form):
    cliente = forms.ModelChoiceField(queryset=clientes.objects.all().order_by('nombre'),to_field_name='nombre')
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
        
        
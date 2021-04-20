import re
import csv
import io
import datetime

def limpiador_bases_interno(texto):
    texto = texto.read()
    texto = texto.replace('.','').replace(',','.')
    texto = re.sub(';\s+-\s+;\s+-\s+;',';;;',texto)
    texto = re.sub(';\s+-\s+;',';;',texto)
    texto = re.sub('\s*-\s\D[a-zA-Z]+\s\D[a-zA-Z]+','',texto)
    texto = texto.replace(' ;',';').replace('; ',';')
    texto = texto.replace(' ; ',';')
    texto = texto.replace(';-;',';0;')
    texto_listo = io.StringIO(texto)
    encabezados_salida = ["fecha","fynsa","otc_tr","nemo","dias","monto","tipo_de_pago","buy","seller","trader_buy","trader_seller","tasa","valor_final","fee_buyer","fee_seller","fee_buyer_moneda","fee_seller_moneda","compra_depo","venta_depo","util_depo","valor_clp","fee_buyer_clp","fee_seller_clp","participante_1","participante_2","tipo_de_cambio","uf"]
    csv_entrada = csv.reader(texto_listo, delimiter = ';')
    texto_salida = io.StringIO()
    next(csv_entrada)
    lista=[]
    for r in csv_entrada:
        indice = [4,5,11,12,13,14,17,18,19,20,21,22,23]
        for i in indice:
            if r[i]=='' or r[i]=='-':
                r[i]=0        
        f = datetime.datetime.strptime(r[0],'%d-%m-%Y')
        f2 = datetime.date.strftime(f,'%Y-%m-%d')
        c = dict(zip(encabezados_salida,[f2,r[1],r[2],r[3],int(r[4]),int(r[5]),r[6],r[7],r[8],r[9],r[10],float(r[11]),int(r[12]),r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[22],r[23],r[24],r[25],0,0]))
        lista.append(c)
    return lista
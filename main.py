import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import numpy as np
import math
import utm
import openrouteservice
import csv
#hora;minuto;tempo_enve;nome;link;tempo;distancia

# get od

data17 = pd.read_csv('data/dados17.csv', dtype={'ZONA_O': str, 'ZONA_D': str}, header=0,delimiter=";", low_memory=False) 
data17 = data17.dropna(subset=['CO_O_X'])
data17['OX'] = data17['CO_O_X'].astype(int)
data17['OY'] = data17['CO_O_Y'].astype(int)
data17['DX'] = data17['CO_D_X'].astype(int)
data17['DY'] = data17['CO_D_Y'].astype(int)

modos17 = {0:'Other',1:'Work',2:'Work',3:'Work',4:'School',5:'Shopping',6:'Health',7:'Entertainment', 8:'House',9:'Seek Employment', 10: 'Personal Issues', 11:'Food'}
data17['MOTIVO_D'] = data17['MOTIVO_D'].replace(modos17)

modos17 = {0:'outros',1:'metro',2:'trem',3:'metro',4:'onibus',5:'onibus',6:'onibus',7:'fretado', 8:'escolar',9:'carro-dirigindo', 10: 'carro-passageiro', 11:'taxi', 12:'taxi-nao-convencional', 13:'moto', 14:'moto-passageiro', 15:'bike', 16:'pe', 17: 'outros'}
data17['MODOPRIN'] = data17['MODOPRIN'].replace(modos17)

data17 = data17[data17['MUNI_O'] == 36]
data17 = data17[data17['MUNI_D'] == 36]
data17 = data17[data17['MODOPRIN'] == 'bike']


sns.violinplot(y="DURACAO", data=data17, palette="muted")
plt.savefig('tempo_real.png', bbox_inches='tight', pad_inches=0.0)
plt.close()


experimentos = [1,2,3,4,5,6,7]
inicio = data17

for exp in experimentos:

    data = pd.read_csv('data/events_' + str(exp) + '.xml', delimiter=";", header=0, low_memory=False) 

    tempo = 'tempo' + str(exp)
    nome = 'nome' + str(exp)

    data[tempo] = data['tempo'] / 60

    new = data['nome'].str.split("_", expand = True) 
    data[nome] = new[1]
    data[nome] = data[nome].astype(int)

    data = data[[nome, tempo]].groupby([nome]).mean().sort_values(by=[tempo]).reset_index()

    if exp == 1:
        inicio = pd.merge(inicio, data, left_index= True, right_on=nome)
    else:
        inicio = pd.merge(inicio, data, left_on= 'nome1', right_on=nome)

    print(inicio)


inicio['media'] = (inicio['tempo1'] + inicio['tempo2'] + inicio['tempo3'] + inicio['tempo4'] + inicio['tempo5'] + inicio['tempo6'] + inicio['tempo7']) / 7


inicio = inicio[['nome1', 'tempo1','tempo2','tempo3','tempo4','tempo5','tempo6','tempo7','media', 'DURACAO']]
inicio.to_csv('teste.csv')

inicio['diferenca_od'] = inicio['DURACAO'] - inicio['media']
inicio['diferenca_od'].hist()
plt.show()
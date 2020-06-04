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

# get first experiment

data = pd.read_csv('data/events_1.xml', delimiter=";", header=0, low_memory=False) 
data['tempo'] = data['tempo'] / 60

new = data['nome'].str.split("_", expand = True) 
data['nome'] = new[1]
data['nome'] = data['nome'].astype(int)

data = data[['nome', 'tempo']].groupby(['nome']).mean().sort_values(by=['tempo']).reset_index()

sns.violinplot(y="tempo", data=data, palette="muted")
plt.savefig('tempo_simulado.png', bbox_inches='tight', pad_inches=0.0)
plt.close()

inicio = pd.merge(data17, data, left_index= True, right_on='nome')

# get second experiment
data = pd.read_csv('data/events_2.xml', delimiter=";", header=0, low_memory=False) 
data['tempo2'] = data['tempo'] / 60

new = data['nome'].str.split("_", expand = True) 
data['nome2'] = new[1]
data['nome2'] = data['nome2'].astype(int)

data = data[['nome2', 'tempo2']].groupby(['nome2']).mean().sort_values(by=['tempo2']).reset_index()

inicio = pd.merge(inicio, data, left_on='nome', right_on='nome2')

# get third experiment
data = pd.read_csv('data/events_3.xml', delimiter=";", header=0, low_memory=False) 
data['tempo3'] = data['tempo'] / 60

new = data['nome'].str.split("_", expand = True) 
data['nome3'] = new[1]
data['nome3'] = data['nome3'].astype(int)

data = data[['nome3', 'tempo3']].groupby(['nome3']).mean().sort_values(by=['tempo3']).reset_index()

inicio = pd.merge(inicio, data, left_on='nome', right_on='nome3')

# get fourth experiment
data = pd.read_csv('data/events_4.xml', delimiter=";", header=0, low_memory=False) 
data['tempo4'] = data['tempo'] / 60

new = data['nome'].str.split("_", expand = True) 
data['nome4'] = new[1]
data['nome4'] = data['nome4'].astype(int)

data = data[['nome4', 'tempo4']].groupby(['nome4']).mean().sort_values(by=['tempo4']).reset_index()

inicio = pd.merge(inicio, data, left_on='nome', right_on='nome4')

inicio['media'] = (inicio['tempo'] + inicio['tempo2'] + inicio['tempo3'] + inicio['tempo4']) / 4 #+ inicio['tempo3'])/3


inicio = inicio[['nome', 'tempo','tempo2','tempo3','tempo4','media', 'DURACAO']]


data_open = pd.read_csv('data/teste_open.csv', delimiter=",", header=0, low_memory=False) 
data_open = data_open[['nome','tempo_open']]
inicio = pd.merge(inicio, data_open[['nome','tempo_open']], left_on='nome', right_on='nome')

inicio['tempo_open'] = inicio['tempo_open'] / 60
inicio['diferenca_open'] = inicio['tempo_open'] - inicio['media']

inicio.to_csv('teste.csv')

inicio['diferenca_open'].hist()
plt.show()


inicio['diferenca_od'] = inicio['DURACAO'] - inicio['media']

inicio['diferenca_od'].hist()
plt.show()
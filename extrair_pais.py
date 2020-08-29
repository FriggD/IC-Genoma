import pandas
import csv
import sys
import numpy as np
import math

ANIMAL_ID = 0
ID_PAI = 1
PAI_GENOMA = 2
ID_MAE = 3
MAE_GENOMA = 4
PATH_35K = 5
PATH_50K = 6
PATH_75K = 7
PATH_90K = 8

class animais:

    
class animal:
    

names = ['id','id_pai','pai_genoma','id_mae', 'mae_genoma', 'path_35k', 'path_50k', 'path_75k', 'path_90k']

dataset = pandas.read_csv('../dados/todos_animais.csv', sep=',', names=names)

animais = dataset.values
# cpms = array[:,0:3]
# biotipo = array[:,3]

f = csv.writer(open('pais.csv', "w"))
f.writerow(animais[0])

Pais_inseridosArr = []

for candidato_pai in animais[1:,]:
    for candidato_filho in animais[1:,]:

        # Captura todos os diferentes Ids do pai (se ele possuir mais de um)
        Ids_pai = candidato_pai[ANIMAL_ID].split(sep=";")

        #  Para cada Id do pai, verifica se ele é pai do candidato_filho
        for Id_pai in Ids_pai:
            if  Id_pai == candidato_filho[ID_PAI]:
                #  È PAI!
                if candidato_pai[ANIMAL_ID] not in Pais_inseridosArr:
                    # Se o pai ainda não foi inserido na lista de pais
                    f.writerow(candidato_pai)
                    Pais_inseridosArr.append(candidato_pai[ANIMAL_ID])
                
        



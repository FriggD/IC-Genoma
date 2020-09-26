# Sumário
#   1. Imports
#   2. Classe Animal
#      2.1. Construtor
#      2.2. Mostrar animais
#      2.3. Exportar pais
#      2.4. Exportar mães
#      2.5. Gerar genoma unico animal
#   3. Instanciação

import numpy as np
import pandas as pd
import csv
from time import sleep
from copy import deepcopy
import random
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

from keras import optimizers
from keras.models import Sequential, load_model
from keras.layers import Dense


DATA_FOLDER = '../Dados'

# import sys
# import numpy as np
# import math

from src.Animal import *
from src.Genomas import Genomas

class AnimaisCtrl:
    # Classe construtor
    def __init__(self):

        self.genomas = Genomas()

        #TODO: Verificar se os arquivos utilizados existem; Se não existirem, crie-os

        #cabeçalho da tabela a ser gerado no arquivo csv
        self.headers = ['Animal_id', 'sexo', 'data_nascimento', 'id_pai', 'id_mae', 'avo_materno', 'tem_filhos', 'genoma_files', 'attrs']
        
        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        self.animais_DF = pd.read_csv(DATA_FOLDER+'/Application/Animais.csv', sep=',', names=self.headers)
                   
        #iniciando o array para poder utilizar o 'append()'.
        self.lista_animais = []

        #Para cada linha no array de dados, excluíndo o cabeçalho
        for linha in self.animais_DF.values:
            #criando uma instancia de animal para cada linha na lista
            self.lista_animais.append(Animal(linha))

    def mostrarAnimais(self):
        #para cada animal na lista de animais
        for animal in self.lista_animais:
            #Mostra as informações do animal. Classe que está no Animal.py
            print(animal)

    #Para não duplicar dados na tabela 'todos_animais'
    def recuperarAnimalPeloNome(self, nome):
        # Buscar o animal na lista de animais que já tenho
        for animal in self.lista_animais:
            if nome in animal.animal_id:
                return animal      

        # Se não for encontrado, retorna False
        return False

    #Para não duplicar dados na tabela 'todos_animais'
    def removerAnimalPeloNome(self, nome):
        # Buscar o animal na lista de animais que já tenho
        for animal_idx, animal in enumerate(self.lista_animais):
            if nome in animal.animal_id:
                self.lista_animais.pop(animal_idx)
                return True 

        # Se não for encontrado, retorna False
        return False

    def inserirNovoAnimal(self, animal):
        animalJaCadastrado = 0
        for nome in animal.animal_id:
            if self.recuperarAnimalPeloNome(nome):
                # Erro! Animal já está cadastrado
                print("Animal já cadastrado")
                return False

        ###### Criar novo animal ######
        #  Adicionar a linha do animal na planilha tabela
        animal_row = pd.Series(animal.toArray(), index=self.headers)
        self.animais_DF = self.animais_DF.append( animal_row, ignore_index=True)

        with open(DATA_FOLDER+'/Application/Animais.csv', 'w') as f:
            self.animais_DF.to_csv(f, header=0)

        #  Adicionar o animal à lista de animais
        self.lista_animais.append(animal)

    def atualizarAnimalCsv(self, animal, old_animal_id = None):
        if old_animal_id:
            self.animais_DF = self.animais_DF.loc[self.animais_DF['Animal_id'] != ";".join(old_animal_id)]
        else:
            self.animais_DF = self.animais_DF.loc[self.animais_DF['Animal_id'] != ";".join(animal.animal_id)]
            
        # Remove animal do Dataframe        
        self.removerAnimalPeloNome(animal.animal_id[0])
       
        self.inserirNovoAnimal(animal)

        with open(DATA_FOLDER+'/Application/Animais.csv', 'w') as f:
            self.animais_DF.to_csv(f, header=0)


    def readAttrFile(self, attr_file):
        file_DataFrame = pd.read_csv(DATA_FOLDER+'/raw/attrs/'+attr_file)

        columns = file_DataFrame.columns.values
        column_classif = []
        column_animal_id = -1

        # Pega informações do arquivo
        print("\n\nInforme sobre as colunas do arquivo:")
        for col_idx, column in enumerate(columns):
            print("A coluna {} é:".format(column))
            try:
                column_opt = int(input("\n   0: Irrelevante\n   1: Animal_id\n   2: Sexo\n   3: Nasc\n   4: Id_Pai\n   5: Id_Mae\n   6: Id_Avo_Materno\n   7: Outro_Id\n   9: Attr\nOpção:"))
            except:
                column_opt = 0

            column_classif.append(column_opt)
            if column_opt == 1:
                column_animal_id = col_idx
            
        if column_animal_id == -1:
            print("ERRO: Coluna animal_id não selecionada")
            return

        cont_animais = 0

        #  Lê o arquivo
        for line in file_DataFrame.values:
            animal = self.recuperarAnimalPeloNome(line[column_animal_id])
          
            if animal:
                temp_animal_id = deepcopy(animal.animal_id)
                cont_animais = cont_animais + 1            
                print("{} Animal {} está na lista de animais".format(cont_animais, line[column_animal_id]))
                for col_idx, col_value in enumerate(line):
                    if column_classif[col_idx] == 1:
                        continue
                    elif column_classif[col_idx] == 2: # Sexo
                        animal.sexo = col_value
                    elif column_classif[col_idx] == 3:  # Nasc
                        animal.nasc = col_value
                    elif column_classif[col_idx] == 4:  # Id_Pai
                        animal.id_pai = col_value
                    elif column_classif[col_idx] == 5:  # Id_Mae
                        animal.id_mae = col_value
                    elif column_classif[col_idx] == 6:  # Id_Avo_Materno
                        animal.avo_materno = col_value
                    elif column_classif[col_idx] == 7:  # Outro_Id
                        animal.add_animal_id(col_value)
                    elif column_classif[col_idx] == 9: # Attr
                        animal.add_attr(columns[col_idx], col_value)
                    else:
                        continue
                
                self.atualizarAnimalCsv(animal, temp_animal_id)





        print(attr_file)
            
    # Extrai o genoma, e adiciona os animais novos na minha lista de animais
    def extrairGenoma(self, genomaFileHandlers, genoma_type):
        # Genoma_folder
        genoma_folder = self.genomas.getFolderById(genoma_type)
        if not(genoma_folder):
            print("Folder Não existe")
            return
               
        #cabeçalho da tabela a ser gerado no arquivo csv
        headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']
        
        aux_nome = 0

        skip_animal = False
        skip_all = False
        recreate_all = False
        
        for file_idx, fileHandler in enumerate(genomaFileHandlers):
            print("Abrindo arquivo {}, {}".format(file_idx,fileHandler[0]))
            sleep(1)

            if fileHandler[1]:
                handler = pd.read_csv(fileHandler[0], usecols=fileHandler[1], chunksize=1000)
            else:
                handler = pd.read_csv(fileHandler[0],  chunksize=1000)            

            #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
            for batchData in handler:
                print('.', end="")
                
                #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
                batch = batchData.values            
                
                #Para cada linha no array de dados, excluíndo o cabeçalho
                for linha in batch:

                    if linha[3] != aux_nome:
                        print("Novo animal: ", linha[3])
                        skip_animal = False
                        aux_nome = linha[3]

                        # Verifica se o Animal já está na lista de animais
                        animal = self.recuperarAnimalPeloNome(aux_nome)

                        if animal:
                            # Se estiver na lista de animais, verifica se o tipo do genoma está incluído em genoma_files do animal
                            
                            if not(str(genoma_type) in animal.genoma_files):
                                #  Se o genoma_Type não estiver no genoma_files do animal, o inclui
                                animal.genoma_files.append(str(genoma_type))
                                print("\nAnimal já estava na lista, porém genoma diferente")
                                self.atualizarAnimalCsv(animal)
                            else:

                                if recreate_all:
                                    skip_animal = False
                                elif skip_all:
                                    skip_animal = True
                                else:
                                    while True:
                                        recreate_opt = int(input("Já possui este genoma para o animal, deseja recriá-lo?\n  1: Sim\n  2: Sim para todos\n  3: Não;\n  4: Não para todos\nOpção:"))
                                        
                                        if recreate_opt == 1:
                                            skip_animal = False
                                        elif recreate_opt == 2:
                                            skip_animal = False
                                            recreate_all = True
                                        elif recreate_opt == 3:
                                            skip_animal = True  
                                        elif recreate_opt == 4:
                                            skip_animal = True                                
                                            skip_all = True
                                        
                                        if recreate_opt in [1,2,3,4]:
                                            break
                        else:
                            # Se animal não existe, inicializa seu valor
                            self.inserirNovoAnimal( Animal([str(linha[3]), None, None, None, None, None, None, str(genoma_type)]) )

                        #arquivo do proprio animal, do genoma
                        if not(skip_animal):
                            try:
                                f_animal_file.close()
                            except:
                                print("\n")

                            f_animal_file = open(DATA_FOLDER + "/Application/Genomas/"+str(genoma_folder)+"/"+str(linha[3]) +'.csv', "w")
                            animal_file = csv.writer(f_animal_file)

                    if not(skip_animal):
                        animal_file.writerow(linha)
                 
            try:
                if f_animal_file:
                    f_animal_file.close()
            except:
                pass            

    def rnaBiotipo(self):
        Animais = []
        Biotipos = []

        for animal in self.lista_animais:
            # biotipo_animal_text = float(animal.get_attr_value('PESO_NASC'))
            biotipo_animal_text = animal.get_attr_value('CLASSE_SOB')

            if str(biotipo_animal_text) in [-1, "-1", "NAN", None]:
                continue
           
            # cria um vetor de animal ,Biotipo
            Animais.append([animal.animal_id[0]])
            # Biotipos.append(biotipo_animal_text)
            Biotipos.append(AnimaisCtrl.getBiotipoVal(biotipo_animal_text))

        Animais_train, Animais_test, Biotipos_train, Biotipos_test = train_test_split(Animais, sklearn.preprocessing.minmax_scale(Biotipos), test_size=0.3, random_state=22)
       
        proceder = 0
        while not(proceder in [1,2]):
            proceder = int(input("Como deseja proceder:\n   1: Carregar Modelo\n   2: Iniciar novo Modelo\n -> "))

        name = ''
        if proceder == 1:
            name = input("Qual o nome do modelo? \n -> ")
            
            classifier = load_model(DATA_FOLDER+"/Application/Models/"+name)
        else:
            name = input("Digite um nome para este modelo\n -> ")

            classifier = Sequential()

            classifier.add(Dense(units=1024, activation = 'relu', input_dim=35338))
            classifier.add(Dense(units=128, activation = 'relu'))
            classifier.add(Dense(units=16, activation = 'relu'))
            classifier.add(Dense(units=16, activation = 'relu'))
            classifier.add(Dense(units=1, activation = 'sigmoid'))

            optimizer = optimizers.Adam(lr=0.001)
            classifier.compile(optimizer = optimizer, loss='binary_crossentropy')

        oquefazer = 0
        while oquefazer in [0,1,2,3,4,5]:
            oquefazer = int(input("O que deseja fazer? \n  1- Testar o Modelo\n  2- Treinar\n  3- Visualizar Dados de Teste\n  4- Visualizar dados de Treinamento  \n  5- Salvar e Sair\n -> "))

            if oquefazer == 1:
                mean_error, predOK = self.testModelKeras(Animais_test, Biotipos_test, classifier)
                print("\n### Erro médio: {:.8f} # {}/{} acertos ({:.2f}% acc)  \n".format(mean_error, predOK, len(Animais_test), (predOK/len(Animais_test))*100), end="", flush=True)
            
            elif oquefazer == 2:
                for generation in range(5):
                    mean_error, predOK = self.testModelKeras(Animais_test, Biotipos_test, classifier)
                    print("\n### Geração {} # Erro médio: {:.8f} # {}/{} acertos ({:.2f}% acc)  \n".format(generation, mean_error, predOK, len(Animais_test), (predOK/len(Animais_test))*100), end="", flush=True)

                    classifier.save(DATA_FOLDER+"/Application/Models/"+name)

                    for batch in range(5):
                        train_batch_X, train_batch_y = self.getTrainBatchData(Animais, Biotipos)
                        classifier.fit(train_batch_X, train_batch_y, batch_size=15, epochs=1)
                    
            elif oquefazer == 3:
                sns.countplot(Biotipos_test)
                plt.show()
            elif oquefazer == 4:
                sns.countplot(Biotipos_train)
                plt.show()
            elif oquefazer == 5:
                break
            else:
                continue

        classifier.save(DATA_FOLDER+"/Application/Models/"+name)

        # np.random.seed(1)

        # syn0 = 2*np.random.random((35338, 100)) -1
        # syn1 = 2*np.random.random((100, 1)) -1
        # syn2 = 2*np.random.random((20, 5)) -1
        # syn3 = 2*np.random.random((5, 5)) -1
        # syn4 = 2*np.random.random((5, 1)) -1

        # for generation in range(1000):            

        #     # ############## Teste ##############
        #     mean_error, predOK = self.testModel(Animais_test, Biotipos_test, [syn0, syn1])         
        #     print("\n### Geração {} # Erro médio: {:.8f} # {}/{} acertos ({:.2f}% acc) # LR {:.4f} # ".format(generation, mean_error, predOK, len(Animais_test), (predOK/len(Animais_test))*100, learningRate), end="", flush=True)

        #     # ############## Treinamento ##############
        #     print("Batch: ",end="", flush=True)
        #     for train_batch in range(10):
        #         print("[{}".format(train_batch), end="")

        #         train_batch_X, train_batch_y = self.getTrainBatchData(Animais, Biotipos)
        #         # print("Shape[0]: \n{}".format(train_batch_X[0].shape))

        #         l0 = train_batch_X
        #         l1 = AnimaisCtrl.sigmoid(np.dot(l0, syn0))
        #         l2 = AnimaisCtrl.sigmoid(np.dot(l1, syn1))
        #         # l3 = AnimaisCtrl.sigmoid(np.dot(l2, syn2))
        #         # l4 = AnimaisCtrl.sigmoid(np.dot(l3, syn3))
        #         # l5 = AnimaisCtrl.sigmoid(np.dot(l4, syn4))

        #         print(".", end="", flush=True)

        #         # l5_error = train_batch_y - l5
        #         # # print("Erro: {}".format(l5_error))

        #         # l5_delta = l5_error * AnimaisCtrl.sigmoid(l5, deriv=True)

        #         # l4_error = l5_delta.dot(syn4.T)
        #         # l4_delta = l4_error * AnimaisCtrl.sigmoid(l4, deriv=True)

        #         # l3_error = l4_delta.dot(syn3.T)
        #         # l3_delta = l3_error * AnimaisCtrl.sigmoid(l3, deriv=True)

        #         l2_error = train_batch_y -l2

        #         # l2_error = l3_delta.dot(syn2.T)
        #         l2_delta = l2_error * AnimaisCtrl.sigmoid(l2, deriv=True)

        #         l1_error = l2_delta.dot(syn1.T)
        #         l1_delta = l1_error * AnimaisCtrl.sigmoid(l1, deriv=True)

        #         print(".", end="", flush=True)

        #         # Atualizando pesos sinápticos   
        #         # syn4 += (l4.T.dot(l5_delta)) * learningRate
        #         # syn3 += (l3.T.dot(l4_delta)) * learningRate
        #         # syn2 += (l2.T.dot(l3_delta)) * learningRate
        #         syn1 += (l1.T.dot(l2_delta))
        #         syn0 += (l0.T.dot(l1_delta)) 

        #         # print("{:.5f}] ".format(np.mean(np.absolute(l5_error.flatten()))), end="", flush=True)
                
        #     learningRate = learningRate* (0.95)

        # print("Treinamento: {}\n Teste: {}\n".format(len(Animais_train), len(Animais_test)))

    def testModelKeras(self, animaisArr, BiotiposArr, classifier):
        batchSize = 60
        animalCount = 0
        batch = 0

        err = np.array([])
        predOK = []
        while (animalCount < len(animaisArr)):
            testeDataX = []
            testeDatay = []
            animais = []
            for i in range(batchSize):
                animalCount += 1
                current_animal = i + (batch*batchSize)
                animais.append([animaisArr[current_animal], BiotiposArr[current_animal]])

                if animalCount >= len(animaisArr):
                    break

            for animal in animais:
                animal_genotipo = []
                testeDatay.append([animal[1]])

                mapa_genotipo = pd.read_csv(DATA_FOLDER+'/Application/Genomas/GGP_Indicus_35K/'+str(animal[0][0])+".csv", usecols=[4,5])
                for line in mapa_genotipo.values:
                    if (line[0] == "A" and line[1] == "B") or (line[0] == "B" and line[1] == "A"):
                        animal_genotipo.append(1)
                    elif line[0] == "A" and line[1] == "A":
                        animal_genotipo.append(2)
                    elif line[0] == "B" and line[1] == "B":
                        animal_genotipo.append(3)
                    else:
                        animal_genotipo.append(5)

                testeDataX.append(np.array(animal_genotipo))

            testeDataX = np.array(testeDataX)
            testeDatay = np.array(testeDatay)

            pred_y = classifier.predict(testeDataX)

            errors = (testeDatay - np.array(pred_y).flatten())     
           
            err = np.concatenate((err, np.absolute(errors).flatten()), axis=0)

            for pred_idx, pred in enumerate(pred_y):
                predOK.append(int(AnimaisCtrl.biotipoClassifOK(testeDatay[pred_idx], pred)))

        return [np.mean(err), np.sum(np.array(predOK))]
   
    def getTrainBatchData(self, animaisArr, BiotiposArr):
        BATCH_SIZE = 120

        animais = []
        biotipoCount = {str(1/12): 0, str(3/12):0, str(5/12): 0, str(7/12): 0, str(9/12): 0, str(11/12): 0}
 
        while (len(animais) < BATCH_SIZE):
            randomAnimal = np.random.randint(0, len(animaisArr)-1)
            if randomAnimal in animais:
                continue

            # animais.append([animaisArr[randomAnimal], BiotiposArr[randomAnimal]])
            # print(randomAnimal)
            if (biotipoCount[str(BiotiposArr[randomAnimal])] < (BATCH_SIZE/6)):
                animais.append([animaisArr[randomAnimal], BiotiposArr[randomAnimal]])
                biotipoCount[ str(BiotiposArr[randomAnimal]) ] += 1

        BatchDataX = []
        BatchDatay = []
        for animal in animais:
            # print("Animal{}".format(animal))
            animal_genotipo = []

            BatchDatay.append([animal[1]])

            mapa_genotipo = pd.read_csv(DATA_FOLDER+'/Application/Genomas/GGP_Indicus_35K/'+str(animal[0][0])+".csv", usecols=[4,5])
            for line in mapa_genotipo.values:
                animal_genotipo.append(AnimaisCtrl.getGenotipoVal(line[0], line[1]))               
               
                    
            BatchDataX.append(np.array(animal_genotipo))

        return np.array(BatchDataX), np.array(BatchDatay)

    # @staticmethod
    # def sigmoid(x, deriv=False):
    #     if deriv == True:
    #         return x*(1-x)

    #     return 1/(1+ np.exp(-x))

    @staticmethod
    def getGenotipoVal(genAB_1, genAB_2):
        if (genAB_1 == "A" and genAB_2 == "B") or (genAB_1 == "B" and genAB_2 == "A"):
            return 0.5
        elif genAB_1 == "A" and genAB_2 == "A":
            return 0.3
        elif genAB_1 == "B" and genAB_2 == "B":
            return 0.7
        else:
            return 0

    @staticmethod
    def biotipoClassifOK(biotipo_real, biotipo_pred):
        # margem = 0.01
        margem = 1/12

        classifOK = (abs(biotipo_real - biotipo_pred) <= margem)
       
        return classifOK
            
    @staticmethod
    def getBiotipoVal(biotipo):
        biotipo =  str(biotipo).upper().strip()
        if biotipo == "DESCARTE":
            return 1/12

        elif biotipo == "INFERIOR":
            return 3/12

        elif biotipo == "STANDARD":
            return 5/12

        elif biotipo == "TOP BEEF":
            return 7/12

        elif biotipo == "TOP FAT":
            return 9/12

        elif biotipo == "PRIME":
            return 11/12

        else:
            print("Erro de biotipo: {}".format(biotipo))


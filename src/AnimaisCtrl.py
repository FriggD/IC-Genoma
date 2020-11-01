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
  
    def make_dataset(self):
        AnimaisArr = []
        FeaturesArr = []

        for animal in self.lista_animais:
            # biotipo_animal_text = float(animal.get_attr_value('PESO_NASC'))
            biotipo_animal_text = animal.get_attr_value('CLASSE_SOB')

            if str(biotipo_animal_text) in [-1, "-1", "NAN", None]:
                continue
           
            # cria um vetor de animal, biotipo
            AnimaisArr.append([animal.animal_id[0]])
            FeaturesArr.append(biotipo_animal_text)

        dataset_name = input("Nomeie o novo dataset:\n-> ")
        dataset_file_open = open(DATA_FOLDER + "/Application/Datasets/"+dataset_name +'.csv', "w")
        dataset_file = csv.writer(dataset_file_open)

        for animal_idx, animal in enumerate(AnimaisArr):
            # print("Animal{}".format(animal))
            genotiposArr = [FeaturesArr[animal_idx]]
            genotipo_file = pd.read_csv(DATA_FOLDER+'/Application/Genomas/GGP_Indicus_35K/'+str(animal[0])+".csv", usecols=[4,5])
            for line in genotipo_file.values:
                genotiposArr.append(AnimaisCtrl.getGenotipoVal(line[0], line[1]))               
               
            # Escreve no arquivo 
            dataset_file.writerow(genotiposArr)

    @staticmethod
    def getGenotipoVal(genAB_1, genAB_2):
        if (genAB_1 == "A" and genAB_2 == "B") or (genAB_1 == "B" and genAB_2 == "A"):
            return 1
        elif genAB_1 == "A" and genAB_2 == "A":
            return 0
        elif genAB_1 == "B" and genAB_2 == "B":
            return 2
        else:
            return 5

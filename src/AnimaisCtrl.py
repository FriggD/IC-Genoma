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
import time
from copy import deepcopy
import random

import concurrent.futures


DATA_FOLDER = '../Dados'

# import sys
# import numpy as np
# import math

from src.Animal import *

class AnimaisCtrl:
    # Classe construtor
    def __init__(self):

        #TODO: Verificar se os arquivos utilizados existem; Se não existirem, crie-os

        #cabeçalho da tabela a ser gerado no arquivo csv
        self.headers = ['Animal_id', 'sexo', 'data_nascimento', 'id_pai', 'id_mae', 'avo_materno', 'tem_filhos', 'attrs']
        
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
                # print("Animal já cadastrado")
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

    def orderAndMapAnimal(self, animal_name, animal_genoma, animal_map):

        # Ordena o genoma por cromossomo e posição
        genoma_header = ["SNP", "Chr", "Pos", "Animal", "Allele1", "Allele2"]
        animal_genoma_ordenado = pd.DataFrame(animal_genoma, columns=genoma_header).sort_values(["Chr", "Pos", "SNP"])

        # escreve genoma ordenado
        with open(DATA_FOLDER + "/Application/Genomas/"+str(animal_name)+".csv", 'w') as f:
            animal_genoma_ordenado.to_csv(f, header=0, index=False)

        # Gera Hash do Mapa do animal
        animal_map_DF = pd.DataFrame(np.matrix(animal_map), columns=["SNP", "Chr", "Pos"])
        animal_map_DF = animal_map_DF.sort_values(["Chr", "Pos", "SNP"])

        aleleString = ""
        for alele in animal_map_DF.values:
            # Concatena Chr e Pos de todos os alelos
            aleleString = aleleString + str(alele[1]) + str(alele[2])

        animal_map_hash = str(hash(aleleString)) # Gerando o Hash 

        # Busca na lista de mapas genéticos já existentes
        map_header = ["name", "hash", "count"]
        maps = pd.read_csv(DATA_FOLDER + "/Application/Maps/index.csv", sep=',', names=map_header)

        # Verificar Se mapa genético do animal_name já existe (comparar hashs)     
        map_repetido = 0
        map_data = maps.values
        for map in map_data:
            if str(map[1]) == animal_map_hash:
                # Se existir, incrementa o número de animais no mapa
                map[2] = map[2]+1
                map_repetido = 1

        # TODO: Se não existir, crie um novo mapa
        if map_repetido == 0:
            map_data = np.append(map_data, [["AutoGenerated-"+str(len(animal_map))+"-"+animal_map_hash, animal_map_hash, str(len(animal_map))]], axis=0)
            with open(DATA_FOLDER + "/Application/Maps/index", 'w') as f:
                pd.DataFrame(np.matrix(map_data)).to_csv(f, header=0, index=False)

            # Escrevendo o mapa
            with open(DATA_FOLDER + "/Application/Maps/AutoGenerated-"+str(len(animal_map))+"-"+animal_map_hash, 'w') as f:
                animal_map_DF.to_csv(f, header=0, index=False)
            
    # Extrai o genoma, e adiciona os animais novos na minha lista de animais
    def extrairGenoma(self, genomaFileHandlers):
        #cabeçalho da tabela a ser gerado no arquivo csv   
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            for fileHandler, result in zip(genomaFileHandlers, executor.map(self.handleGenomaFile, genomaFileHandlers)):
                print("{} Levou {} segundos".format(fileHandler[0], str(result)))
  
    def handleGenomaFile(self, fileHandler):
        headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']

        aux_nome = 0
        animal_mapping = []
        new_animal = False
        start = time.time()

        print("Abrindo arquivo, {}".format(fileHandler[0]))

        if fileHandler[1]:
            handler = pd.read_csv(fileHandler[0], usecols=fileHandler[1], chunksize=1000)
        else:
            handler = pd.read_csv(fileHandler[0], chunksize=1000)            

        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        for batchData in handler:
            
            #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
            batch = batchData.values            
            
            #Para cada linha no array de dados, excluíndo o cabeçalho
            for linha in batch:
                if linha[3] != aux_nome:
                    # Se linha[3] != aux_nome, significa que foi esgotado os alelos do último animal a ser analisado,
                    # e iniciou com outro animal

                    # Finaliza o último animal (se aux_nome != 0)
                    if aux_nome != 0:                           

                        self.orderAndMapAnimal(aux_nome, ANIMAL_GENOMA, animal_mapping)

                        try: f_animal_file.close()
                        except: pass                       

                        animal_mapping = []
                    
                    aux_nome = linha[3]

                    # Verifica se o Animal já está na lista de animais
                    animal = self.recuperarAnimalPeloNome(aux_nome)

                    if animal:
                        print("Animal já existente: ", linha[3])
                        new_animal = False

                        # Se estiver na lista de animais, pega a lista de genoma do animal já criado
                        genoma_header = ["SNP", "Chr", "Pos", "Animal", "Allele1", "Allele2"]
                        try:
                            ANIMAL_GENOMA = pd.read_csv(DATA_FOLDER + "/Application/Genomas/"+str(aux_nome)+".csv", sep=',', names=genoma_header).values
                        except:
                            ANIMAL_GENOMA = 0   

                    else:
                        new_animal = True
                        print("Novo animal: ", linha[3])

                        # Se animal não existe, cria o objeto do animal
                        self.inserirNovoAnimal( Animal([str(linha[3]), None, None, None, None, None, None]) )

                        # Inicializa o numpy da tabela genoma do animal
                        ANIMAL_GENOMA = 0
                    
                    # f_animal_file = open(DATA_FOLDER + "/Application/Genomas/"+str(linha[3]) +'.csv', "w")
                    # animal_file = csv.writer(f_animal_file)

                # ADICIONANDO ALELO NA LISTA

                # TODO: verificar se genoma do animal já possui o alelo criado
                if not(new_animal):
                    # genoma_linha_encontrada = (ANIMAL_GENOMA[:, 0] == linha[0]).nonzero()
                    # genoma_linha_encontrada =  np.where(ANIMAL_GENOMA[:, 0] == linha[0]).nonzero()
                    genoma_linha_encontrada =  np.where(ANIMAL_GENOMA[:, 0] == linha[0])
                    if len(genoma_linha_encontrada[0]) > 0:
                        # Linha encontrada 
                        # Se o registrado for missing, completa o valor
                        genoma_linha = ANIMAL_GENOMA[genoma_linha_encontrada[0]][0]
                        if str(genoma_linha[4]) == "-" and str(genoma_linha[5] == "-"):
                            # print("Genoma Missing, completando...", genoma_linha[4], genoma_linha[5])
                            # Genoma missing, atualiza os valores da tabela
                            ANIMAL_GENOMA[genoma_linha_encontrada][0][4] = linha[4] # Allele1 - AB
                            ANIMAL_GENOMA[genoma_linha_encontrada][0][5] = linha[5] # Allele2 - AB
                    else:
                        # Linha não encontrada, adiciona a row
                        try:
                            ANIMAL_GENOMA = np.append(ANIMAL_GENOMA, [linha], axis=0)
                        except:
                            ANIMAL_GENOMA = np.array([linha])
                else:
                    # Animal novo, não precisa verificar se row já existe
                    try:
                        ANIMAL_GENOMA = np.append(ANIMAL_GENOMA, [linha], axis=0)
                    except:
                        ANIMAL_GENOMA = np.array([linha])

                # constrói mapa de genoma desse animal 
                animal_mapping.append([linha[0], linha[1], linha[2]])
                
        try:
            if f_animal_file:
                f_animal_file.close()
        except: pass    

        try:
            self.orderAndMapAnimal(aux_nome, ANIMAL_GENOMA, animal_mapping)
        except: pass   

        end = time.time()

        return (end - start) 

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

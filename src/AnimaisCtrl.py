# Sumário
#   1. Imports
#   2. Classe Animal
#      2.1. Construtor
#      2.2. Mostrar animais
#      2.3. Exportar pais
#      2.4. Exportar mães
#      2.5. Gerar genoma unico animal
#   3. Instanciação

import pandas as pd
import csv

DATA_FOLDER = '../Data'

# import sys
# import numpy as np
# import math

from src.Animal import *
# from src.Genomas import Genomas

class AnimaisCtrl:
    # Classe construtor
    def __init__(self):

        #TODO: Verificar se os arquivos utilizados existem; Se não existirem, crie-os

        #cabeçalho da tabela a ser gerado no arquivo csv
        self.headers = ['Animal_id', 'sexo', 'data_nascimento', 'id_pai', 'id_mae', 'avo_materno', 'tem_filhos', 'genoma_files']
        
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
        for animal in self.lista_animais:
            if nome in animal.animal_id:
                self.lista_animais.remove(Animal)
                return True 

        # Se não for encontrado, retorna False
        return False

    def inserirNovoAnimal(self, animal):
        animalJaCadastrado = 0
        for nome in animal.animal_id:
            if self.recuperarAnimalPeloNome(nome):
                # Erro! Animal já está cadastrado
                return False

        ###### Criar novo animal ######
        #  Adicionar a linha do animal na planilha tabela
        animal_row = pd.Series(animal.toArray())
        self.animais_DF = self.animais_DF.append( animal_row, ignore_index=True)

        with open(DATA_FOLDER+'/Application/Animais.csv', 'w') as f:
            self.animais_DF.to_csv(f, header=0)

        #  Adicionar o animal à lista de animais
        self.lista_animais.append(animal)

    def atualizarAnimalCsv(self, animal):

        self.animais_DF = self.animais_DF[self.animais_DF.Animal_id != animal.animal_id]


        self.animais_DF.at(animal.animal_nr, animal.toArray())
        with open(DATA_FOLDER+'/Application/Animais.csv', 'w') as f:
            self.animais_DF.to_csv(f, header=0)
            


    # Extrai o genoma, e adiciona os animais novos na minha lista de animais
    def extrairGenoma(self, genoma_filename, genoma_type):
               
        #cabeçalho da tabela a ser gerado no arquivo csv
        headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']
        
        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pd.read_csv(DATA_FOLDER+'/Input/'+genoma_filename, sep=',', names=headers)

        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values

        #iniciando o array para poder utilizar o 'append()'.
        self.lista_info_animal = []

        aux_nome = 0
        #Para cada linha no array de dados, excluíndo o cabeçalho
        for linha in dataArr[1:,]:
            
            if linha[3] != aux_nome:
                aux_nome = linha[3]

                # Verifica se o Animal já está na lista de animais
                animal = self.recuperarAnimalPeloNome(aux_nome)

                if animal:
                    # Se estiver na lista de animais, verifica se o tipo do genoma está incluído em genoma_files do animal
                    
                    if not(genoma_type in animal.genoma_files):
                        #  Se o genoma_Type não estiver no genoma_files do animal, o inclui
                        animal.genoma_files.append(genoma_type)
                        self.atualizarAnimalCsv(animal)

                else:
                    # Se animal não existe, inicializa seu valor
                    self.inserirNovoAnimal( Animal([linha[3], None, None, None, None, None, str(genoma_type)]) )

                #arquivo do proprio animal, do genoma
                try:
                    f_animal_file.close()
                except:
                    print("\n")

                f_animal_file = open(DATA_FOLDER + "/Application/Genomas/"+ linha[3] +'.csv', "w")
                animal_file = csv.writer(f_animal_file)

            animal_file.writerow(linha)

            

        if f_animal_file:
            f_animal_file.close()


# animais_obj = AnimaisCtrl()

# animais_obj.extrairGenoma()



# animais_obj.mostrarAnimais()
# animais_obj.exportarPais()
# animais_obj.exportarMaes()
# animais_obj.recuperarAnimalPeloNome('MASTER KA')



# Inserindo novo animal
# animal_teste = Animal(['531', None, None, None, None, None, None, None, None])
# animal_teste.mostrar_informacoes()
# animais_obj.inserirNovoAnimal(animal_teste)

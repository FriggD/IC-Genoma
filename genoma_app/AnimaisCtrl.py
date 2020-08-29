# Sumário
#   1. Imports
#   2. Classe Animal
#      2.1. Construtor
#      2.2. Mostrar animais
#      2.3. Exportar pais
#      2.4. Exportar mães
#      2.5. Gerar genoma unico animal
#   3. Instanciação

import pandas
import csv
# import sys
# import numpy as np
# import math

from Animal import *

class AnimaisCtrl:
    # Classe construtor
    def __init__(self):
        #cabeçalho da tabela a ser gerado no arquivo csv
        self.headers = ['Animal_id', 'sexo','id_pai', 'id_mae', 'tem_filhos']
        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pandas.read_csv('../../dados/todos_animais.csv', sep=',', names=self.headers)
        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values
        #iniciando o array para poder utilizar o 'append()'.
        self.lista_animais = []

        #Para cada linha no array de dados, excluíndo o cabeçalho
        for linha in dataArr[1:,]:
            #criando uma instancia de animal para cada linha na lista
            self.lista_animais.append(Animal(linha))

    def mostrarAnimais(self):
        #para cada animal na lista de animais
        for animal in self.lista_animais:
            #Mostra as informações do animal. Classe que está no Animal.py
            animal.mostrar_informacoes()

    #Sempre que um animal aparecer na coluna dos pais
    def exportarPais(self):
        #Abrir o arquivo dos pais na pasta de outputs no modo escrita
        f = csv.writer(open('Output/pais.csv', "w"))
        #escreve o cabeçalho
        f.writerow(self.headers)
        #inicializa o array
        Pais_inseridosArr = []
        #Para cada pai na lista de animais
        for candidato_pai in self.lista_animais:
            #para cada filho na lista de animais
            for candidato_filho in self.lista_animais:              

                #  Para cada Id do pai, verifica se ele é pai do candidato_filho
                for Id_pai in candidato_pai.animal_id:
                    if  Id_pai == candidato_filho.id_pai:
                        #  È PAI!
                        if candidato_pai.animal_id not in Pais_inseridosArr:
                            # Se o pai ainda não foi inserido na lista de pais
                            f.writerow(candidato_pai.toArray())
                            Pais_inseridosArr.append(candidato_pai.animal_id)
    
    def exportarMaes(self):
        f = csv.writer(open('Output/maes.csv', "w"))
        f.writerow(self.headers)

        Maes_inseridasArr = []

        for candidata_mae in self.lista_animais:
            for candidato_filho in self.lista_animais:              

                #  Para cada Id da mae, verifica se ela é mae do candidato_filho
                for Id_mae in candidata_mae.animal_id:
                    if  Id_mae == candidato_filho.id_mae:
                        #  È MÃE!
                        if candidata_mae.animal_id not in Maes_inseridasArr:
                            # Se a mae ainda não foi inserida na lista de maes
                            f.writerow(candidata_mae.toArray())
                            Maes_inseridasArr.append(candidata_mae.animal_id)

    #
    #def gerarGenomaUnicoAnimal(self):

    #Para não duplicar dados na tabela 'todos_animais'
    def recuperarAnimalPeloNome(self, nome):
        animal_encontrado = 0

        # Buscar o animal na lista de animais que já tenho
        for animal in self.lista_animais:
            if nome in animal.animal_id:
                 animal_encontrado = animal

        # Se encontrado, retorna o animal
        if animal_encontrado:
            return animal_encontrado

        # Se não, retorna False
        return False

    def inserirNovoAnimal(self, animal):
        animalJaCadastrado = 0
        for nome in animal.animal_id:
            if self.recuperarAnimalPeloNome(nome):
                # Erro! Animal já está cadastrado
                return False

        ###### Criar novo animal ######
        #  Adicionar a linha do animal na planilha tabela
        animais_file = csv.writer(open('../../dados/todos_animais.csv', "a"))
        animais_file.writerow(animal.toArray())
        
        #  Adicionar o animal à lista de animais
        self.lista_animais.append(animal)

    # Extrai o genoma, e adiciona os animais novos na minha lista de animais
    def extrairGenoma(self):

        genoma_filename = input("Qual o endereço do arquivo do genoma? \n")

        genoma_type = input("Este arquivo genoma é de qual tipo? \n  1: 35k; \n  2: 50k; \n  3: 75k; \n  4: 90k;\nOpção:")
        
        checagem_headers = input("Verifique se as colunas da tabela estão configurada da seguinte forma:\n  ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']\n  Em formato csv separado por ,\n(y/n): ")
                
        #cabeçalho da tabela a ser gerado no arquivo csv
        headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']
        
        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pandas.read_csv('genoma_filename', sep=',', names=headers)

        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values

        #iniciando o array para poder utilizar o 'append()'.
        self.lista_info_animal = []

        aux_nome = 0
        #Para cada linha no array de dados, excluíndo o cabeçalho
        for linha in dataArr[1:,]:
            
            if linha[3] != aux_nome:
                aux_nome = linha[3]
                
                #arquivo do proprio animal, do genoma
                animal_file = csv.writer(open('Output/Infos_animais/'+ linha[3] +'.csv', "w"))

            animal_file.writerow(linha)

            print(linha[3])


animais_obj = AnimaisCtrl()

animais_obj.extrairGenoma()



# animais_obj.mostrarAnimais()
# animais_obj.exportarPais()
# animais_obj.exportarMaes()
# animais_obj.recuperarAnimalPeloNome('MASTER KA')



# Inserindo novo animal
# animal_teste = Animal(['531', None, None, None, None, None, None, None, None])
# animal_teste.mostrar_informacoes()
# animais_obj.inserirNovoAnimal(animal_teste)

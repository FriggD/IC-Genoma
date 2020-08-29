#Gerar um arquivo das informações de cada animal

#Sumário
#   1.Imports

import pandas
import csv

class Informacoes:
    # Classe construtor
    def __init__(self):
        #cabeçalho da tabela a ser gerado no arquivo csv
        self.headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']
        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pandas.read_csv('../../dados/Animais/379517_Deoxi_BOVZEBV01_20180718_FinalReport_1.csv', sep=',', names=self.headers)
        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values
        #iniciando o array para poder utilizar o 'append()'.
        self.lista_info_animal = []

        #cria uma instancia
        animais_file = csv.writer(open('../../dados/todos_animais.csv', "a"))

        aux_nome = 0
        #Para cada linha no array de dados, excluíndo o cabeçalho
        for linha in dataArr[1:,]:
            
            if linha[3] != aux_nome:
                aux_nome = linha[3]
                animais_file.writerow([linha[3],None,None,None,None, 'Output/Infos_animais/'+ linha[3] +'.csv'])
                #arquivo do proprio animal, do genoma
                animal_file = csv.writer(open('Output/Infos_animais/'+ linha[3] +'.csv', "w"))

            animal_file.writerow(linha)

            print(linha[3])

    def extrairInfos(self):
         #Abrir o arquivo dos pais na pasta de outputs no modo escrita
        f = csv.writer(open('Output/Infos_animais/'+  +'.csv', "w"))
        #escreve o cabeçalho
        f.writerow(self.headers)


info = Informacoes()

import pandas
import csv

from src.AnimaisCtrl import DATA_FOLDER

class Genomas:

    def __init__(self):
        self.headers = ['Genoma']

        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pandas.read_csv(DATA_FOLDER+'/Application/genoma_types', sep=',', names=self.headers)
    
        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values

        #iniciando o array para poder utilizar o 'append()'.
        self.lista_genomas = []
        for linha in dataArr[1:,]:
            self.lista_genomas.append( Genoma(linha) )


class Genoma:
    def __init__(self, dataArr):
        self.id = dataArr[0]
        self.type = dataArr[1]
        self.folder = dataArr[1]

    def toOptionString(self):
        return "{} => {}".format(self.id, self.type)


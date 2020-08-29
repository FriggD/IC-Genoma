import pandas
import csv

from AnimaisCtrl import DATA_FOLDER

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

    def addGenoma(self, id, type, folder):
        new_genoma = Genoma([id, type, folder])
        self.lista_genomas.append( new_genoma )

        genoma_file = csv.writer(open(DATA_FOLDER+'/Application/genoma_types', "a"))
        genoma_file.writerow( new_genoma.toArray() )


class Genoma:
    def __init__(self, dataArr):
        self.id = dataArr[0]
        self.type = dataArr[1]
        self.folder = dataArr[1]

    def toOptionString(self):
        return "{} => {}".format(self.id, self.type)

    def toArray(self):
        return [self.id, self.type, self.folder]


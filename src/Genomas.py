import pandas
import csv
import os

from src.AnimaisCtrl import DATA_FOLDER

GENOMA_TYPES_FILE = DATA_FOLDER+"/Application/genoma_types.csv"

class Genomas:
    def __init__(self):
        self.headers = ['Id','Genoma','Folder']

        #Conjunto de dados recebe o que o 'pandas' lê do arquivo csv que está especifícado no caminho, utilizando o separados (,).
        dataset = pandas.read_csv(GENOMA_TYPES_FILE, sep=',', names=self.headers)
    
        #Um array de dados recebe os valores que estão no conjunto de dados do arquivo acima.
        dataArr = dataset.values

        self.num_genomas = 0

        #iniciando o array para poder utilizar o 'append()'.
        self.lista_genomas = []
        for linha in dataArr[0:,]:
            self.lista_genomas.append( Genoma(linha) )
            self.num_genomas += 1

    def getFolderById(self, id):
        print("Buscando ", id)
        for genoma in self.lista_genomas:
            if genoma.id == id:
                return genoma.folder
        
        return False

    def addGenoma(self, type, folder):
        # TODO: Verificar se tipo de genoma ou o folder já existem

        # Verificar se a pasta com o nome desejado já existe
        caminho = DATA_FOLDER+"/Application/Genomas/"+folder 
        # Se não existir, cria a pasta
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        new_genoma = Genoma([self.num_genomas+1, type, folder])

        self.num_genomas += 1
        
        self.lista_genomas.append( new_genoma )

        genoma_file = csv.writer(open(GENOMA_TYPES_FILE, "a"))
        genoma_file.writerow( new_genoma.toArray() )

        # Retorna o ID do novo genoma
        return self.num_genomas


class Genoma:
    def __init__(self, dataArr):
        self.id = dataArr[0]
        self.type = dataArr[1]
        self.folder = dataArr[2]

    def toOptionString(self):
        return "{} => {}".format(self.id, self.type)

    def toArray(self):
        return [self.id, self.type, self.folder]


from src.models.Models_loader import Animal, Animal_nome, Mapa, Mapa_marcador, Marcador
from src.configuration.config import DATA_FOLDER

import os
import pandas as pd

headers = ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']

SNP = 0
CHR = 1
POSITION = 2
ANIMAL = 3
ALLELE1 = 4
ALLELE2 = 5

class extrairGenomaController:
    # def iniciarExtração(self):
    

    def __init__(self):
        print("init extrairGenomaController")

        self.genoma_folder = '' # Diretório com os genomas a serem analisados
        self.fileHandlers = [] # Lista de FileHandlers do arquivos source de genoma

        # Receber input do usuário
        self.input()

        # A partir da pasta indicada, cria um file handler para cada arquivo
        self.getFileHandlers()

        # Para cada arquivo a ser analisado, faça
        for fileHandler in self.fileHandlers:
            results = extrairGenomaController.extrairGenoma(fileHandler)

    def input(self):
        # Pedir ao Usuário o diretório onde estão localizados os arquivos
        # O usuário deverá informar o diretório com caminho relativo à pasta Dados/raw
        self.genoma_folder = input("\nQual o endereço da pasta a ser scaneada? \n Endereço(Relativo à /raw): ")        
        

    def getFileHandlers(self):
        # Para cada arquivo dentro do folder especificado, faça
        for file in os.listdir(DATA_FOLDER+'/raw/'+ self.genoma_folder):
            # Verifica se o arquivo é .csv
            if file.endswith(".csv"):
                # Lê as 5 primeiras linhas do arquivo
                file_DF = pd.read_csv(DATA_FOLDER+'/raw/'+self.genoma_folder+'/'+file, nrows=5)     
                columns = file_DF.columns.values

                try:
                    if ( list(columns) == ['SNP_Name', 'Chr', 'Position', 'Sample_ID', 'Allele1 - AB', 'Allele2 - AB']):
                        self.fileHandlers.append([DATA_FOLDER+'/raw/'+self.genoma_folder+'/'+file, False])
                    elif columns[0] == 'SNP Name' and columns[1] == 'Chr' and columns[2] == 'Position' and columns[3] == 'Sample ID' and columns[8] == 'Allele1 - AB' and columns[9] ==  'Allele2 - AB':
                        self.fileHandlers.append([DATA_FOLDER+'/raw/'+self.genoma_folder+'/'+file, [0,1,2,3,8,9]])
                except:
                    pass
    
    @staticmethod
    def extrairGenoma(fileHandler):

        # Para não sobrecarregar a memória, serão lidos 1000 linhas por vez, 
        # Este bloco de dados chama-se batch
        if fileHandler[1]:
            handler = pd.read_csv(fileHandler[0], usecols=fileHandler[1], chunksize=1000)
        else:
            handler = pd.read_csv(fileHandler[0], chunksize=1000)

        # Inicializa variável que armazena o animal sendo analisado correntemente
        cur_animal = ''

        for batch in handler:

            batchData = batch.values

            for linha in batchData:   

                # Verifica se o bloco de dados do animal anterior finalizou
                if linha[ANIMAL] != cur_animal:
                    # Detectado novo animal 



        """ 
            TODO: trazer para cá a lógica de chamada de função que foi criada dentro de app, isso inclui:
            lógica da função def extrairGenoma(self):

            @staticmethod
            def getFileHandlersFromFolder(folder):

        """


        """
        TODO: Trazer para cá as lógicas dentro de AnimaisCtrl referente à extração de genoma
            def handleGenomaFile(self, fileHandler):
            def extrairGenoma(self, genomaFileHandlers):
            def orderAndMapAnimal(self, animal_name, animal_genoma, animal_map):
        """

        # TODO: Mudar as lógicas para trabalhar no banco ao invés em arquivo
  
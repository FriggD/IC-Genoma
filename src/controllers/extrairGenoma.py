from src.database.GenomaDB import Animal, Mapa, AnimalMapa, Marcador, Mapa_marcador
from src.configuration.config import DATA_FOLDER

import os
import pandas as pd
import sqlalchemy_mixins

# headers = ['SNP Name_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']

# "SNP Name" = 0
# CHR = 1
# POSITION = 2
# ANIMAL = 3
# ALLELE1 = 4
# ALLELE2 = 5

class extrairGenomaController:
    # def iniciarExtração(self):
    
    # d = dict(zip(L1,L2))
    def __init__(self):
        print("init extrairGenomaController")

        self.genoma_folder = '' # Diretório com os genomas a serem analisados
        self.fileHandlers = [] # Lista de FileHandlers do arquivos source de genoma
        self.MapHash = ""
        self.DFmap = []

        # Receber input do usuário
        self.input()

        # A partir da pasta indicada, cria um file handler para cada arquivo
        self.getFileHandlers()

        # Para cada arquivo a ser analisado, faça
        for fileHandler in self.fileHandlers:
            results = self.extrairGenoma(fileHandler)


        # # Multiprocessamento
        # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        #     for fileHandler, result in zip(genomaFileHandlers, executor.map(self.handleGenomaFile, genomaFileHandlers)):
        #         print("{} Levou {} segundos".format(fileHandler[0], str(result)))


    def input(self):
        # Pedir ao Usuário o D onde estão localizados os arquivos
        # O usuário deverá informar o diretório com caminho relativo à pasta Dados/raw
        # self.genoma_folder = input("\nQual o endereço da pasta a ser scaneada? \n: ")        
        self.genoma_folder = "../Dados/"        
        

    # region retorna uma ponteiro para cada arquivo dentro da pasta indicada
    def getFileHandlers(self):
        # Para cada arquivo dentro da pasta indicada
        print(os.getcwd())
        for file in os.listdir(self.genoma_folder):
            # Se o arquivo for do tipo txt, faça
            if file.endswith("txt"):    
                file_path = str(self.genoma_folder)+str(file)

                handler = self.getAndTrimHeader(file_path)
                if handler:
                    self.fileHandlers.append(handler)
                    return True
                else:
                    return False
    # endregion

    # region remove as informações acima do header e retorna o ponteiro para o arquivo junto com o header
    def getAndTrimHeader(self, file_path):
        # Cria o ponteiro para o arquivo
        fp = open(file_path, 'r')

        # para cada linha no ponteiro para o arquivo
        for line in fp:
            try:
                genCols = line.split('\t')
                if (genCols[0] == 'SNP Name'):
                    return {"file": fp, "header": genCols}
            except:
                print("\nHouve um erro ao tentar procurar o Header")
                return False
        return False
    # endregion

    # region mapAnmial
    def mapAnimal(self, animal_dict):
        # print(f"{animal_dict['nome']} com {len(animal_dict['genotypes'])} marcadores. {animal_dict['genotypes'][0]['SNP Name']}")
        animal_encontrado = True
        try:
            Animal.find_or_fail(animal_dict['nome'])
        except sqlalchemy_mixins.activerecord.ModelNotFoundError:
            print(f"Animal {animal_dict['nome']} não encontrado no banco de dados (ModelNotFoundError)")
            animal_encontrado = False

        if animal_dict['sample'] == 0:
            self.CreateMapHash(animal_dict['genotypes'])

            # Verifica se o mapa já está cadastrado
            try:
                Mapa.find_or_fail(self.MapHash)            
            except sqlalchemy_mixins.activerecord.ModelNotFoundError:
                mapa_nome = input(f"Foi detectado um mapa ainda não cadastrado com {len(self.DFmap)} marcadores. Insira um nome para esse mapa.")
                Mapa.create(id=self.MapHash, nome=mapa_nome, snp_count=len(self.DFmap))
                for idx, marcador in self.DFmap.iterrows():
                    #TODO: Cadastrar os marcadores
                    #TODO: Cadastrar Mapa_Marcador para cada marcador 

    # endregion

    # region CreateMapHash
    def CreateMapHash(self, genotypes):
        MapString = ""
        # region criação de dataframe e separação de x e y 
        DFgenotypes = pd.DataFrame(genotypes)
        # Garantir que não haverá uma dupla de chr e pos duplicados
        DFgenotypes = DFgenotypes.drop_duplicates(subset=["Chr","Position"])
        DFgenotypes_x = DFgenotypes.loc[DFgenotypes["Chr"]=="X"]
        DFgenotypes_y = DFgenotypes.loc[DFgenotypes["Chr"]=="Y"]
        DFgenotypes = DFgenotypes.loc[~DFgenotypes["Chr"].isin(["X","Y"])]
        # endregion
       
        # region casting de string para numerico das colunas chr e pos
        DFgenotypes["Chr"] = pd.to_numeric(DFgenotypes["Chr"])
        DFgenotypes["Position"] = pd.to_numeric(DFgenotypes["Position"])
        DFgenotypes_x["Position"] = pd.to_numeric(DFgenotypes_x["Position"])
        DFgenotypes_y["Position"] = pd.to_numeric(DFgenotypes_y["Position"])
        # endregion

        # region ordenação dos dataframes por chr, pos e snp name
        DFgenotypes = DFgenotypes.sort_values(by=['Chr','Position','SNP Name'])
        DFgenotypes_x = DFgenotypes_x.sort_values(by=['Position','SNP Name'])
        DFgenotypes_y = DFgenotypes_y.sort_values(by=['Position','SNP Name'])
        # endregion

        # region concatenação de dataframes
        DFgenotypes = pd.concat([DFgenotypes, DFgenotypes_x,DFgenotypes_y])
        # print(DFgenotypes) 
        # endregion       

        # region criação do hash
        for idx, genotype in DFgenotypes.iterrows():
            MapString += f"{genotype['Chr']}{genotype['Position']}{genotype['SNP Name']}"
        
        self.DFmap = DFgenotypes
        self.MapHash = hash(MapString)
        # endregion
    # endregion

    # region [extrairGenoma]
    def extrairGenoma(self, fileHandler):
        # fileHandler['header']
        # fileHandler['file']

        samples = 0
        aux_animal_nome = ""
        aux_animal_genotypes = []

        # Para cada linha do arquivo a ser analisado, faça
        for line in fileHandler["file"]:
            rows = line.split("\t")
            marcador_dict = dict(zip(fileHandler["header"],rows))
            if(marcador_dict["Sample ID"] != aux_animal_nome):
                if not(aux_animal_nome == ""):                    
                    self.mapAnimal({
                        "nome": aux_animal_nome,
                        "genotypes": aux_animal_genotypes,
                        "sample": samples
                    })
                    samples += 1

                aux_animal_nome = marcador_dict["Sample ID"]
                aux_animal_genotypes = []

            # print(fileHandler['header'])
            aux_animal_genotypes.append({
                "SNP Name": marcador_dict["SNP Name"],
                "Chr": marcador_dict["Chr"],
                "Position": marcador_dict["Position"],
                "Allele1 - Forward": marcador_dict["Allele1 - Forward"],
                "Allele2 - Forward": marcador_dict["Allele2 - Forward"],
                "Allele1 - AB": marcador_dict["Allele1 - AB"],
                "Allele2 - AB": marcador_dict["Allele2 - AB"]
            })
    # endregion
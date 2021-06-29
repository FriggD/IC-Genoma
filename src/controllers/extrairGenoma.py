from src.database.GenomaDB import Animal, Mapa, Animal_mapa, Marcador, Mapa_marcador, session
from src.configuration.config import DATA_FOLDER
from src.helpers.logger import logger

import os
import pandas as pd
import sqlalchemy_mixins
import hashlib
from tqdm import tqdm

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
        logger.debug("init extrairGenomaController")

        self.genoma_folder = '' # Diretório com os genomas a serem analisados
        self.fileHandlers = [] # Lista de FileHandlers do arquivos source de genoma
        self.MapHash = ""
        self.mapId = 0
        self.DFmap = []

        # Receber input do usuário
        self.input()

        # A partir da pasta indicada, cria um file handler para cada arquivo
        try:
            self.getFileHandlers()        

            # Para cada arquivo a ser analisado, faça
            for fileHandler in self.fileHandlers:
                logger.info(f"(extrairGenoma, __init__) Extraindo dados do arquivo {fileHandler}")
                results = self.extrairGenoma(fileHandler)
        except:
            logger.error("Erros!", exc_info=True)


        # # Multiprocessamento
        # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        #     for fileHandler, result in zip(genomaFileHandlers, executor.map(self.handleGenomaFile, genomaFileHandlers)):
        #         print("{} Levou {} segundos".format(fileHandler[0], str(result)))


    def input(self):
        # Pedir ao Usuário o D onde estão localizados os arquivos
        # O usuário deverá informar o diretório com caminho relativo à pasta Dados/
        # self.genoma_folder = input("\nQual o endereço da pasta a ser scaneada? \n: ")    #TODO: Descomentar    
        self.genoma_folder = "../Dados/" # TODO: Comentar
        

    # region retorna uma ponteiro para cada arquivo dentro da pasta indicada
    def getFileHandlers(self):
        """
            ? Popula a lista self.fileHandlers com os arquivos que serão usados para popular o banco
                list.dir() lista todos os arquivos dentro de uma pasta.
                for file ... fará a iteração sobre todos os itens, fazendo verificações neles antes de adicioná-los na lista
                * Verificação 1: Verifica se o arquivo é .txt
                * Verificação 2: getAndTrimHeader
        """
        # Para cada arquivo dentro da pasta indicada
        for file in os.listdir(self.genoma_folder):
            # Se o arquivo for do tipo txt, faça
            if file.endswith("txt"):    
                file_path = str(self.genoma_folder)+str(file)

                handler = self.getAndTrimHeader(file_path)
                if handler:
                    self.fileHandlers.append(handler)
    # endregion

    # region remove as informações acima do header e retorna o ponteiro para o arquivo junto com o header
    def getAndTrimHeader(self, file_path):
        # Cria o ponteiro para o arquivo
        logger.debug(f"Trimmando {file_path}")
        num_lines = sum(1 for line in open(file_path,'r'))

        fp = open(file_path, 'r')
        # para cada linha no ponteiro para o arquivo
        for line in fp:
            try:
                genCols = line.split('\t')
                if (genCols[0] == 'SNP Name'):
                    return {"file": fp, "header": genCols, "count": num_lines}
            except:
                logger.error("\nHouve um erro ao tentar procurar o Header", exc_info=True)
                return False
        return False
    # endregion

    # region mapAnmial
    def mapAnimal(self, animal_dict):
        # print(f"{animal_dict['nome']} com {len(animal_dict['genotypes'])} marcadores. {animal_dict['genotypes'][0]['SNP Name']}")
        animal_encontrado = True
        try:
            animal = Animal.find_or_fail(animal_dict['nome'])
        except sqlalchemy_mixins.activerecord.ModelNotFoundError:
            logger.debug(f"Animal {animal_dict['nome']} não encontrado no banco de dados (ModelNotFoundError)")
            animal_encontrado = False
        if not(animal_encontrado):
            # ! Cadastra o animal no Banco
            animal = Animal.create(id=animal_dict['nome'])

        # region Mapa
        if animal_dict['sample'] == 0:
            self.CreateMapHash(animal_dict['genotypes'])

            # Verifica se o mapa já está cadastrado
            mapa = Mapa.find(self.MapHash)
            if mapa == None:
                mapa_nome = input(f"\nFoi detectado um mapa ainda não cadastrado com {len(self.DFmap)} marcadores. Insira um nome para esse mapa:\n Nome: ")

                # ! Grava o Mapa
                mapa = Mapa.create(id=self.MapHash, nome=mapa_nome, snp_count=len(self.DFmap))

                for idx, marcador in self.DFmap.iterrows():

                    try:
                        # ! Cadastrar os marcadores
                        if(Marcador.find(marcador['SNP Name']) == None):
                            Marcador.create(snp=marcador['SNP Name'])
                            logger.debug(f"Criando marcador {marcador['SNP Name']}")
                        else:
                            logger.debug(f"Marcador {marcador['SNP Name']} existente")

                        # ! Cadastrar Mapa_Marcador para cada marcador 
                        Mapa_marcador.create(snp=marcador['SNP Name'], mapa_id=mapa.id, chromossome=marcador['Chr'], position=marcador['Position'])
                    except:
                        logger.warning(f"Marcador {marcador['SNP Name']} Já está cadastrado")
                    
            self.mapId = mapa.id
        # endregion

        # region Animal_Mapa
        try:
            # ! Verifica se registro existe, se não exisir grava
            animal_mapa = Animal_mapa.where(animal_id=animal.id, mapa_id=self.mapId).all()
            if len(animal_mapa) == 0:
                Animal_mapa.create(animal_id=animal.id, mapa_id=self.mapId)

        except Exception as e:
            logger.error("Um erro inesperado ocorreu", exc_info=True)

        # TODO
        self.updateAnimalGenomaFile(animal_dict)

        session.commit()

        # endregion

    # endregion

    def updateAnimalGenomaFile(self, animal_dict):
        """
            ? Atualiza os novos marcadores ao arquivo de genoma do animal
            Se o animal já possuir um arquivo de genoma, faz um merge do genoma atual com o que está vindo
            se não possuir, só cria o arquivo com o genoma novo
            @param animal_dict['nome']
            @param animal_dict['genotypes']
            @param animal_dict['sample']
        """
        genotypesDF = self.sortAndFilterGenotypes(animal_dict['genotypes'])

        logger.debug(f"(extrairGenoma, updateAnimalGenomaFile) Criando arquivo genoma para o animal {animal_dict['nome']}")

        genotypesDF.to_pickle(self.getAnimalGenomaFilePath(animal_dict['nome']), compression='zip')

    # region CreateMapHash
    def CreateMapHash(self, genotypes):
        MapString = ""
        
        DFgenotypes = self.sortAndFilterGenotypes(genotypes) 

        # region criação do hash
        hashGenerator = hashlib.md5()
        for idx, genotype in DFgenotypes.iterrows():
            MapString = f"{genotype['Chr']}{genotype['Position']}{genotype['SNP Name']}"
            hashGenerator.update(MapString.encode('utf-8'))
        
        self.DFmap = DFgenotypes
        self.MapHash = hashGenerator.hexdigest()
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
        for line in tqdm(fileHandler["file"], total=fileHandler['count'], desc="Lendo linhas"):
            rows = line.split("\t")
            marcador_dict = dict(zip(fileHandler["header"], rows))
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

    # region utils
    def animalHasGenomaFile(self, animal_name):
        """
            Verifica se o animal já possui um arquivo de genoma iniciado para ele
        """
        return os.path.isfile(self.getAnimalGenomaFilePath(animal_name))

    def getAnimalGenomaFilePath(self, animal_name):
        if not(os.path.isdir(f"Computed/animais/{self.mapId}")):
            os.mkdir(f"Computed/animais/{self.mapId}")
        return f"Computed/animais/{self.mapId}/{animal_name}.zip"

    def sortAndFilterGenotypes(self, genotypes):
        DFgenotypes = pd.DataFrame(genotypes)

        # region criação de dataframe e separação de x e y 
        # Garantir que não haverá uma dupla de chr e pos duplicados
        DFgenotypes = DFgenotypes.drop_duplicates(subset=["Chr","Position"])
        DFgenotypes = DFgenotypes.drop_duplicates(subset=["SNP Name"], keep='last')
        DFgenotypes = DFgenotypes.loc[DFgenotypes["Chr"]!="0"]
        DFgenotypes = DFgenotypes.loc[DFgenotypes['Position']!="0"]
        DFgenotypes_x = DFgenotypes.loc[DFgenotypes["Chr"]=="X"]
        DFgenotypes_y = DFgenotypes.loc[DFgenotypes["Chr"]=="Y"]
        DFgenotypes_mt = DFgenotypes.loc[DFgenotypes["Chr"]=="MT"]
        DFgenotypes = DFgenotypes.loc[~DFgenotypes["Chr"].isin(["X","Y", "MT"])]
        # endregion
       
        # region casting de string para numerico das colunas chr e pos
        DFgenotypes["Chr"] = pd.to_numeric(DFgenotypes["Chr"])
        DFgenotypes["Position"] = pd.to_numeric(DFgenotypes["Position"])
        DFgenotypes_x["Position"] = pd.to_numeric(DFgenotypes_x["Position"])
        DFgenotypes_y["Position"] = pd.to_numeric(DFgenotypes_y["Position"])
        DFgenotypes_mt["Position"] = pd.to_numeric(DFgenotypes_mt["Position"])
        # endregion

        # region ordenação dos dataframes por chr, pos e snp name
        DFgenotypes = DFgenotypes.sort_values(by=['Chr','Position'])
        DFgenotypes_x = DFgenotypes_x.sort_values(by=['Position'])
        DFgenotypes_y = DFgenotypes_y.sort_values(by=['Position'])
        DFgenotypes_mt = DFgenotypes_mt.sort_values(by=['Position'])
        # endregion

        DFgenotypes = pd.concat([DFgenotypes, DFgenotypes_x, DFgenotypes_y, DFgenotypes_mt])

        return DFgenotypes
    # endregion
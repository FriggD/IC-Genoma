
# -----------------------------------------------------------------------
# Lib import
import argparse, sys
import pandas as pd
import os
import csv
import concurrent.futures
import time

# -----------------------------------------------------------------------
# Imports Libs

# Argument list from commandline
argv = []


def getFilesExtension(ext):
    return (f for f in os.listdir() if f.endswith('.' + ext))

#Classe de entrada
class App:
    # Inicialização da aplicação
    def __init__(self):
        self.createGenotypeFile()
        self.populateGenotypeFile()

    def createGenotypeFile(self):
        genotypeHeader = ['ID', 'Chip', 'Genotypes']

        with open(argv.output, "w") as f:
            csv_writer = csv.writer(f, delimiter=' ')
            csv_writer.writerow(genotypeHeader)

    def populateGenotypeFile(self):
        fileHandlers = App.getFileHandlers()
        for file in fileHandlers:
            genotypes = self.handleGenotypeFile(file)
            with open(argv.output, 'a') as f:
                csv_w = csv.writer(f, delimiter=" ")
                csv_w.writerows(genotypes)

        # with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        #     for fileHandler, result in zip(fileHandlers, executor.map(self.handleGenotypeFile, fileHandlers)):
        #         with open(argv.output, a) as f:
        #             print(f"Finalizado arquivo {fileHandler}")
        #             csv_w = csv.writer(csv_file)
        #             csv_w.writerows(result)
        
    def handleGenotypeFile(self, genotype_file):
        genotypes = []

        print(f"Extraindo genotypes de {genotype_file}")
        gen_f, header = self.getAndTrimHeader(open(genotype_file, 'r'))
         
        if header[8] != "Allele1 - AB" or header[9] != "Allele2 - AB": print(f"Arquivo {genotype_file} com headers incorretos: {header}")
        elif argv.debug: print("Headers do arquivo batem!")

        animalName = ""
        animalArr = []
        for line in gen_f:
            genCols = line.split('\t')

            if animalName != genCols[3]:
                if not(animalName == ""): 
                    if argv.debug: print(f"Mapeando animal {animalName}")
                    start = time.time()
                    genotypes.append( self.mapAnimal(animalArr, header, animalName) )
                    end = time.time()
                    print(f"Animal {animalName} mapeado em {end-start} segundos")
                    time.sleep(0.1)

                animalArr = []                    
                animalName = genCols[3]
            
            animalArr.append(genCols)

        genotypes.append( self.mapAnimal(animalArr, header, animalName) )

        return genotypes
        
    def mapAnimal(self, animalArr, header, animal_name):
        # animalArr:
            # -> Lista, cada posição é um marcador do animal (Linha do arquivo .txt)
        # print(f"AnimalArr: {animalArr[0]}")
        # header:
            # Cabeçalho da "Lista dos animais" ,eg cabeçalho da coluna 0 do animalArr será o header[0]
        # print(f"Header: {header}")
        # print(argv.map)


        # animalArr e header são usados para gerar o DataFrame do pandas, logo em seguida (Gera uma tabelinha)
        # print(header)
        genotype = ""
        animalDF = pd.DataFrame(animalArr, columns=header)

        # # Filtra os registros com cromossomo 0, Y, X e MT
        animalDF = animalDF.loc[animalDF['Chr'] != '0'].loc[animalDF['Chr'] != 'MT']
        # .loc[animalDF['Chr'] != 'Y'].loc[animalDF['Chr'] != 'X']  
        animalDF.set_index('SNP Name', inplace=True)

        mapFile = open(argv.map, 'r')
        try: 
            (next(mapFile)) # Pula o cabeçalho do map
        except:
            pass
        
        # Para cada marcador no mapa, faça     map[0]   map[1]      map[2]...
        # Gera String de genótipó do animal : "5        1           2           5           2   1   2   5"
        for line in mapFile:
            try:
                marcadorArr = line.split(' ')                
            except:
                print("Erro ao ler marcador")

            # Procura o marcador no animal
            try:
                marcador_animal = animalDF.loc[marcadorArr[0]]
                animal_encontrado = True
            except KeyError:
                animal_encontrado = False

            if not(animal_encontrado):
                # caiu neste if, significa que o marcador não foi encontrado no animal
                genotype += "5"
                if argv.debug: print(f"{marcadorArr[0]} - [ N, N ] => 5")
            
            else:
                # Se caiu neste else, o marcador foi encontrado
                # Verifica os alelos

                Allele1 = marcador_animal["Allele1 - AB"]
                Allele2 = marcador_animal["Allele2 - AB"]
                valor0125 = App.allelesABTo0125(Allele1, Allele2)

                if argv.debug: print(f"{marcadorArr[0]} - [ {Allele1}, {Allele2} ] => {valor0125}")

                genotype += str(valor0125)
            
        if argv.debug: print(f"Finalizando de mapear animal {animal_name}")
        return [animal_name, argv.chip, genotype]


    @staticmethod
    def allelesABTo0125(AB1, AB2):        
        if AB1 not in(["A", "B"]) or AB2 not in ["A", "B"]: return 5      
        if AB1 == "A" and AB2 == "A": return 0           
        if AB1 == "B" and AB2 == "B": return 2    
        return 1

    @staticmethod
    def getAndTrimHeader(fp):
        for line in fp:      
            try:
                genCols = line.split('\t')
                if (genCols[0] == 'SNP Name'):
                    return [fp, genCols]
            except:
                print("Houve um erro ao tentar procurar o Header") 

    @staticmethod
    def getFileHandlers():
        fileHandlers = []

        for file in os.listdir(argv.genotype_folder):
            if file.endswith("txt"):                   
                fileHandlers.append(str(argv.genotype_folder)+str(file))

        return fileHandlers
    
   
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, help='Enable debug mode', default=0)

    parser.add_argument('--output', type=str, help='Arquivo de saída', default="./genotypes.csv")
    parser.add_argument('--chip', type=int, help='Arquivo de saída', default=1)
    parser.add_argument('--map', type=str, help='Mapa de referência', default="./map.csv")
    parser.add_argument('--genotype-folder', type=str, help='Pasta onde estão localizados os arquivos de genotypes', default="./")

	# parser.add_argument('--loc', type=int, help='Help text', default=0)		
	# parser.add_argument('--betha', type=float, help='Help text', default=0)
	# parser.add_argument('--seriesName', type=str, help='Help text', default="Default")

    return parser.parse_args(argv)

if __name__ == "__main__":
    # First, parse arguments from commandLine
    argv = parse_arguments(sys.argv[1:])

    app = App()

    © 2021 GitHub, Inc.
    Terms
    Privacy
    Security
    Status
    Docs

    Contact GitHub
    Pricing
    API
    Training
    Blog
    About


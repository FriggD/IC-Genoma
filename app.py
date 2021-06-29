# IMPORTS   
import pandas as pd
import os
import csv
import src.database.GenomaDB

from src.controllers.extrairGenoma import extrairGenomaController as extGenController

#Classe de entrada
class App:
    # inicialização
    def __init__(self):
        # Verificações de inicialização
        # Verifica se a estrutura de pastas dos dados existe
        # Verifica se os arquivos necessários estão criados
        self.menu()

    #menu
    def menu(self):
        opt = 1
        while opt != 0:
            print("\n\n\n\n\n##### MENU:")
            print("### O que você quer fazer? ")

            print(" # ( 0 ): Sair do Programa")
            print(" # ( 1 ): Extrair Genoma")
            # print(" # ( 2 ): Converter .txt para .csv (pasta inteira)")
            # print(" # ( 3 ): Importar attributos de animais")
            # print(" # ( 4 ): Gerar dataset Biotipo")
            
            try:
                opt = int(input("Digite sua Opção: "))
            except:
                continue
            
            if opt == 1:
                print("Aqui você está extraindo Genoma!")
                extGenController()
                
                # self.extrairGenoma()
            # elif opt == 2:
            #     App.convertTXT()
            # elif opt == 3:
            #     attr_File = input("Digite o nome do arquivo de atributos:\n-> ")
            #     self.animaisCtrl.readAttrFile(attr_File)
            # elif opt == 4:
            #     self.animaisCtrl.make_dataset()
            # elif opt ==5:
                
    

    # def extrairGenoma(self):
    #     folder = input("\nQual o endereço do arquivo do genoma? \n Endereço: ")

    #     genomaFileHandlers = App.getFileHandlersFromFolder(folder)
               
    #     self.animaisCtrl.extrairGenoma(genomaFileHandlers)

    # @staticmethod
    # def convertTXT():
    #     for file in os.listdir(DATA_FOLDER+'/raw/txt'):
    #         if file.endswith(".txt"):
    #             print("Convertendo arquivo: {}".format(file))

    #             headerFound = False
    #             header =  ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']             

    #             csv_file = open(DATA_FOLDER+'/raw/csv/'+ file.split('.')[0]+".csv", "w")
    #             csv_w = csv.writer(csv_file)
    #             csv_w.writerow(header)

    #             fp = open(DATA_FOLDER+'/raw/txt/'+ file, 'r')
    #             for line_idx, line in enumerate(fp):
    #                 splitted = line.split('\t');
    #                 if headerFound:                       
    #                     csv_w.writerow([splitted[headers_idx[0]], splitted[headers_idx[1]], splitted[headers_idx[2]], splitted[headers_idx[3]], splitted[headers_idx[4]], splitted[headers_idx[5]]])
    #                 else:
    #                     try:
    #                         if (splitted[0] == 'SNP Name' and splitted[1] == 'Chr' and splitted[2] == 'Position' and splitted[3] == 'Sample ID' and splitted[8] == 'Allele1 - AB', splitted[9] ==  'Allele2 - AB'):
    #                             headers_idx = [0,1,2,3,8,9]
    #                             headerFound = True
    #                     except:
    #                         continue     

    #                 # if line_idx == 10:
    #                 #     break

    #             if not(headerFound):
    #                 print("Header não encontrado para arquivo: {}".format(file))
    #             csv_file.close()

    # @staticmethod
    # def getFileHandlersFromFolder(folder):
    #     fileHandler = []

    #     for file in os.listdir(DATA_FOLDER+'/raw/'+folder):
    #         if file.endswith(".csv"):   
    #             file_DataFrame = pd.read_csv(DATA_FOLDER+'/raw/'+folder+'/'+file, nrows=5)     
    #             # GGP_Indicus_35K
    #             columns = file_DataFrame.columns.values
                
    #             try:
    #                 if ( list(columns) == ['SNP_Name', 'Chr', 'Position', 'Sample_ID', 'Allele1 - AB', 'Allele2 - AB']):
    #                     fileHandler.append([DATA_FOLDER+'/raw/'+folder+'/'+file, False])
    #                 elif columns[0] == 'SNP Name' and columns[1] == 'Chr' and columns[2] == 'Position' and columns[3] == 'Sample ID' and columns[8] == 'Allele1 - AB' and columns[9] ==  'Allele2 - AB':
    #                     fileHandler.append([DATA_FOLDER+'/raw/'+folder+'/'+file, [0,1,2,3,8,9]])
    #             except:
    #                 pass

    #     return fileHandler

                


if __name__ == "__main__":
    app = App()
   




# IMPORTS   
from src.AnimaisCtrl import AnimaisCtrl
from src.Genomas import Genomas

#Classe de entrada
class App:
    # inicialização
    def __init__(self):
        self.animaisCtrl = AnimaisCtrl()
        self.genomas = Genomas()
        self.menu()
    #menu
    def menu(self):
        opt = 1
        while opt != 0:
            print("\n\n\n\n\n##### MENU:")
            print("### O que você quer fazer? ")

            print(" # ( 0 ): Sair do Programa")
            print(" # ( 1 ): Extrair animais de um arquivo de Genoma")
            # print(" # ( 0 ): Sair do Programa")
            # print(" # ( 0 ): Sair do Programa")
            
            opt = int(input("Digite sua Opção: "))
            
            if opt == 1:
                self.extrairGenoma()
    #
    def criarGenoma(self):
        genoma_type = input("\nDigite o tipo do Genoma, eg: 35k; 65k...\n Tipo:")
        genoma_folder = input("\nDigite o nome de diretório para esta base de Genoma:\n Diretório:")
        #Retorna a função addGenoma que está no Genoma.py
        return self.genomas.addGenoma(genoma_type, genoma_folder)

    def extrairGenoma(self):
        #genomaOptString é uma função que está no Genoma.py
        genomaOptString = "  0 => Não está nesta lista, criar novo\n"
        for genoma in self.genomas.lista_genomas:
            genomaOptString += "  "+ genoma.toOptionString()+"\n"

        genoma_filename = input("\nQual o endereço do arquivo do genoma? \n Endereço: ")

        genoma_type = int(input("\nEste arquivo genoma é de qual tipo? \n"+genomaOptString+" Opção: "))
        if genoma_type == 0:
            genoma_type = self.criarGenoma()
        
        checagem_headers = input("\nVerifique se as colunas da tabela estão configurada da seguinte forma:\n  ['SNP_Name','Chr','Position','Sample_ID', 'Allele1 - AB', 'Allele2 - AB']\n  Em formato csv separado por ,\n(y/n): ")
            
        if checagem_headers.lower().strip() == 'y':
            print("Extraindo Genoma...")
            self.animaisCtrl.extrairGenoma(genoma_filename, genoma_type)

if __name__ == "__main__":
    app = App()
   




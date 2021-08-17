from sqlalchemy.sql.expression import select
from src.helpers.logger import logger
from src.database.GenomaDB import Mapa, Animal_mapa, Mapa_marcador, BaseDados, session
from itertools import combinations, groupby
from operator import attrgetter
from sqlalchemy_mixins import JOINED, SUBQUERY
from time import sleep
from tqdm import tqdm
import uuid
import os

import pandas as pd

class Phasing:

    def __init__(self):
        """
        """
        logger.debug("(Phasing, __init__)")

        self.selectedMarkers = []
        self.rejectedMarkers = []
        self.selectedIndividuals = []
        self.rejectedIndividuals = []


        self.baseDados = self.SelecionarUnphased()
        self.getBase()

        self.maxMarkerMissingFreq = self.getMaxMarkerMissingFreq()
        self.maxIndividualMissingFreq = self.getMaxIndividualMissingFreq()

        self.phase()
        # print(self.base)
        # print(self.mapa)

    # region Métodos principais
    def phase(self):
        self.selectMarkers()
        self.selectIndividuals()

        # print("Marcadores Removidos: ", self.rejectedMarkers)
        # print('Animais Removidos:', self.rejectedIndividuals)

        self.sepChr()
        self.getChrLegends()

        
        self.baseDados.update(tipo='phased')
        session.commit()

        # print(self.base)
        # print(self.mapa)
    

    def selectMarkers(self):
        
        for rowIndex, row in self.base.iterrows():
            total = 0
            missing = 0
            for colIndex, value in row.items():
                a1, a2 = value.split('|')
                if a1 == '-': missing += 1
                if a2 == '-': missing += 1
                total += 2
            
            if (missing / total) <= (self.maxMarkerMissingFreq):
                self.selectedMarkers.append(rowIndex)
            else:
                self.rejectedMarkers.append(rowIndex)

        self.mapa = self.mapa.loc[self.mapa['snp'].isin(self.selectedMarkers)]
        self.base = self.base.loc[self.selectedMarkers]


    def selectIndividuals(self):  
        for rowIndex, row in self.base.T.iterrows():
            total = 0
            missing = 0
            for colIndex, value in row.items():
                a1, a2 = value.split('|')
                if a1 == '-': missing += 1
                if a2 == '-': missing += 1
                total += 2
            
            if (missing / total) <= (self.maxIndividualMissingFreq):
                self.selectedIndividuals.append(rowIndex)
            else:
                self.rejectedIndividuals.append(rowIndex)

        self.base = self.base.T.loc[self.selectedIndividuals].T

    def getChrLegends(self):
        for chr in self.base:           

            chr_legend = []
            for index, [snp, row] in enumerate(chr['genotypes'].iterrows()):
                alleles_count = [0, 0, 0]              
                alleles = ['', '']

                for animal_id, value in row.items():
                    for al in value.split('|'):

                        if al == alleles[0] or alleles[0] == '':
                            alleles[0] = al
                            alleles_count[0] += 1
                        elif al == alleles[1] or alleles[1] == '':
                            alleles[1] = al
                            alleles_count[1] += 1
                        elif al == '-':
                            alleles_count[2] += 1
                        else:
                            print("DEU MERDA MANO!!!!!!")
                            sleep(10)

                    # print(f'{snp} - {animal_id} - {value}')
                    # sleep(1)
                missing = alleles_count[2]
                if alleles_count[0] >= alleles_count[1]:
                    a1 = alleles[0]
                    a2 = alleles[1]
                    maf = alleles_count[1] / (alleles_count[0] + alleles_count[1])
                else:
                    a1 = alleles[1]
                    a2 = alleles[0]
                    maf = alleles_count[0] / (alleles_count[0] + alleles_count[1])

                pos = chr['mapa'].iloc[index]['position']
                chr_legend.append(['snp', pos, a1, a2, missing, maf])
                # print(f'{snp}, {pos}, {alleles}, {alleles_count}, {a1}, {a2}, {maf}')

            # Guarda a lenda do chr como pickle
            pd.DataFrame(chr_legend, columns=['snp', 'position', 'a1', 'a2', 'missing', 'MAF']) \
                .to_pickle(self.getBaseDadosFilePath(self.baseDados)+'/chr_'+str(chr['chr'])+'_legend.zip', compression='zip')   

        pass

    def sepChr(self):
        # Para cada cromossomo, identificar os marcadores que pertencem a ele
        #   Filtrar da base de dados por essa lista de marcadores
        aux_db = []
        for chr in self.chrArr:
            mapa_chr = (self.mapa.loc[self.mapa['chromossome'] == chr])
            marcadores_chr = mapa_chr['snp'].tolist()

            base = self.base.loc[self.base.index.isin(marcadores_chr)]
            aux_db.append({
                'chr': chr,
                'genotypes': base,
                'mapa': mapa_chr
            })

            # Gravar o mapa do chr com pickle
            mapa_chr.to_pickle(self.getBaseDadosFilePath(self.baseDados)+'/chr_'+str(chr)+'_mapa.zip', compression='zip')   

            # Gravar a base do chr com Pickle
            base.to_pickle(self.getBaseDadosFilePath(self.baseDados)+'/chr_'+str(chr)+'_genotypes.zip', compression='zip')   

        self.base = aux_db
    # endregion

    # region Utils
    def getBase(self):
        filepath = self.getBaseDadosFilePath(self.baseDados)
        self.base = pd.read_pickle(filepath+'/genotypes.zip', compression='zip')
        self.mapa = pd.read_pickle(filepath+'/mapa.zip', compression='zip')
        self.chrArr = self.mapa['chromossome'].unique()

    def getBaseDadosFilePath(self, baseDados):
        if not(os.path.isdir(f"Computed/bases/{baseDados.uuid}")):
            os.mkdir(f"Computed/bases/{baseDados.uuid}")
        return f"Computed/bases/{baseDados.uuid}"
    # endregion
    
    # region Interface
    def SelecionarUnphased(self):
        logger.debug("(Phasing, SelecionarUnphased)")

        bases = BaseDados.where(tipo='unphased').order_by(BaseDados.created_at.desc()).all()

        print('-'*50)
        print("\n#####  Escolha um dataset para Phasing: ")  
        for base_idx, base in enumerate(bases):
            print(f"    # ( {base_idx} ): {base}")

        opt_valido = False
        while not(opt_valido):
            opt = int(input("  # Opção: "))
            opt_valido = opt < len(bases)

        return bases[opt]

    def getMaxMarkerMissingFreq(self):
        logger.debug("(Phasing, getMaxMarkerMissingFreq)")

        maxFreq = input("\n#####  Informe o limitador de frequência de Missing por Marcador (0-100%): ")

        try:
            maxFreqVal = float(maxFreq)
            if maxFreqVal < 0 or maxFreqVal > 100:
                print("Erro, valor digitado inválido")
                return self.getMaxMarkerMissingFreq()
        except:
            print("Erro, valor digitado inválido")
            return self.getMaxMarkerMissingFreq()

        return maxFreqVal/100

    def getMaxIndividualMissingFreq(self):
        logger.debug("(Phasing, getMaxIndividualMissingFreq)")

        maxFreq = input("\n#####  Informe o limitador de frequência de Missing por Animal (0-100%): ")

        try:
            maxFreqVal = float(maxFreq)
            if maxFreqVal < 0 or maxFreqVal > 100:
                print("Erro, valor digitado inválido")
                return self.getMaxIndividualMissingFreq()
        except:
            print("Erro, valor digitado inválido")
            return self.getMaxIndividualMissingFreq()

        return maxFreqVal/100
    # endregion

        
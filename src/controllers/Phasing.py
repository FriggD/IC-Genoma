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

    # region Métodos principais
    def phase(self):
        self.selectMarkers()
        self.selectIndividuals()
        print("Marcadores Removidos: ", self.rejectedMarkers)
        print('Animais Removidos:', self.rejectedIndividuals)
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
    # endregion

    # region Utils
    def getBase(self):
        filepath = self.getBaseDadosFilePath(self.baseDados)
        self.base = pd.read_pickle(filepath+'.zip', compression='zip')
        self.mapa = pd.read_pickle(filepath+'_mapa.zip', compression='zip')
        self.chrArr = self.mapa['chromossome'].unique()

    def getBaseDadosFilePath(self, baseDados):
        if not(os.path.isdir(f"Computed/bases")):
            os.mkdir(f"Computed/bases")
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

        
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

class gerarDataset:

    def __init__(self):
        logger.debug("(gerarDataset, __init__)")

        self.baseDados = None
        self.gerarBaseDados()

    def gerarBaseDados(self):
        logger.debug("(gerarDataset, gerarBaseDados)")

        print('\n\n')

        self.baseDados = self.selecionarDataset()
        self.montarDados()


    # region 
    def selecionarDataset(self):
        logger.debug("(gerarDataset, selecionarDataset)")

        print("#####  Escolha um possível dataset: ")  

        possiveisDatasets = []

        mapas = Mapa.all()
        combinacoesArr = [combinations(mapas, i) for i in range(1, len(mapas)+1)]

        combinacoes = []
        for combinacao in combinacoesArr: combinacoes += combinacao

        # TODO: Melhorar performance
        for j, comb in enumerate(combinacoes):
            comb_name = ""
            for i, mapa in enumerate(comb):
                if i == 0:
                    marcadores = Mapa_marcador.where(mapa_id=mapa.id).all()
                else:
                    comb_name += "+"
                comb_name += mapa.nome.replace(' ', '_').lower()
                
                marcadores = Mapa_marcador.where(mapa_id=mapa.id, snp__in=list(map(lambda x: x.snp, marcadores))).all()

            animais_count = Animal_mapa.where(mapa_id__in=list(map(lambda x: x.id, comb))).count()

            possiveisDatasets.append({
                'num': j, 
                'mapas': comb, 
                'base': comb_name, 
                'animais': animais_count, 
                'marcadores': marcadores,
                'snpArr': [marcador.snp for marcador in marcadores]
            })
            # return possiveisDatasets[0]
            print(f"    # ( {j} ): {comb_name:<25}; nº animais: {animais_count:<6}; nº marcadores: {len(marcadores):<6}")
        
        opt_valido = False
        while not(opt_valido):
            opt = int(input("  # Opção: "))
            opt_valido = opt < len(possiveisDatasets)

        return possiveisDatasets[opt]
    # endregion


    def montarDados(self):
        #              'Animal_x'  'Animal_y'
        # 'BVND0123'      A|T
        # 'BVND0124'      C|G

        #                Animal1, Animal2, Animal3 ...
        # Marcador 1       A|T      A|T
        # Marcador 2
        # Marcador 3
        # ...

        animais = Animal_mapa.where(mapa_id__in=list(map(lambda x: x.id, self.baseDados['mapas']))).order_by(Animal_mapa.mapa_id).all()
        mapas_animaisArr = [dict({k: list(mapa)}) for k, mapa in groupby(animais, attrgetter('mapa_id'))]

        for mapa_idx, m in enumerate(mapas_animaisArr):
            animaisGenArr = []
            animaisArr = []
            marcadoresArr = []

            m_id = list(m)[0] 
            animal_idx = -1
            for animal in tqdm(animais):

                if animal.mapa_id != m_id:
                    continue
                else:
                    animal_idx += 1

                filepath = self.getAnimalGenomaFilePath(animal.animal_id, animal.mapa_id)
                animal_genotypes = pd.read_pickle(filepath, compression='zip')

                # region                              
                animal_x_DF = pd.DataFrame([{'snp': genotype['SNP Name'], animal.animal_id: (f"{genotype['Allele1 - Forward']}|{genotype['Allele2 - Forward']}")} for _, genotype in animal_genotypes.iterrows()])
                animal_x_DF.set_index('snp', inplace=True)
                marcadoresArr = animal_x_DF.T.columns
                animaisArr.append(animal.animal_id)
              
                animaisGenArr.append(animal_x_DF.T.values.tolist()[0])

                # if animal_idx > 40:
                    # break
                # endregion

            if mapa_idx == 0:
                BASEDADOS = pd.DataFrame(animaisGenArr, index=animaisArr, columns=marcadoresArr).filter(self.baseDados['snpArr'])
            else:
                BASEDADOS = pd.concat(
                    [
                        BASEDADOS, 
                        pd.DataFrame(animaisGenArr, index=animaisArr, columns=marcadoresArr) \
                            .filter(self.baseDados['snpArr']) \
                            [BASEDADOS.columns.tolist()] # Força a ordenação padrão desde o primeiro registro
                    ]                             
                )

        baseDados = BaseDados.create(
            uuid= uuid.uuid4().hex,
            nome=self.baseDados['base'],
            tipo='unphased',
            marcadores= len(self.baseDados['marcadores']),
            animais= self.baseDados['animais']
        )

        BASEDADOS.T.to_pickle(self.getBaseDadosFilePath(baseDados)+'/genotypes.zip', compression='zip')     

        mapa = pd.DataFrame([i.__dict__ for i in self.baseDados['marcadores'] ]).filter(['snp', 'position','chromossome'])
        mapa.to_pickle(self.getBaseDadosFilePath(baseDados)+'/mapa.zip', compression='zip')     

        session.commit()

    def getAnimalGenomaFilePath(self, animal_name, mapa_id):
        if not(os.path.isdir(f"Computed/animais/{mapa_id}")):
            os.mkdir(f"Computed/animais/{mapa_id}")
        return f"Computed/animais/{mapa_id}/{animal_name}.zip"

    
    def getBaseDadosFilePath(self, baseDados):
        if not(os.path.isdir(f"Computed/bases/{baseDados.uuid}")):
            os.mkdir(f"Computed/bases/{baseDados.uuid}")
        return f"Computed/bases/{baseDados.uuid}"
    




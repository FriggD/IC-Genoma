from src.helpers.logger import logger
from src.database.GenomaDB import Animal, BaseDados, Mapa, Animal_mapa, Marcador

class dadosAnalyticsController:
    # def iniciarExtração(self):
    
    def __init__(self):
        logger.debug("(dadosAnalyticsController, __init__)")
        print('\n')
        self.animaisAnalytics()
        self.marcadoresAnalytics()
        self.mapasAnalytics()
        self.basesAnalytics()

    def animaisAnalytics(self):
        logger.debug("(dadosAnalyticsController, animaisAnalytics)")
        print('-'*50)

        print("ANIMAIS:    ", Animal.where().count())

    def mapasAnalytics(self):
        logger.debug("(dadosAnalyticsController, mapasAnalytics)")
        mapas = Mapa.all()
        print("MAPAS:      ", len(mapas))

        print('-'*50)
        print("Lista de mapas:")
        for mapa in mapas:
            animais_mapa = Animal_mapa.where(mapa_id=mapa.id).all()
            print(f' - {mapa.nome}')
            print(f'    - {mapa.snp_count} marcadores')
            print(f'    - {len(animais_mapa)} animais')

    def basesAnalytics(self):
        logger.debug("(dadosAnalyticsController, basesAnalytics)")
        bases = BaseDados.where().order_by(BaseDados.created_at.desc()).all()
        
        print('-'*50)
        print("BASES:      ", len(bases))
        print("Lista de Bases de Dados:")
        for base in bases:
            print(f' - {base.nome} | {base.created_at}')
            print(f'    - Tipo: {base.tipo}')
            print(f'    - {base.marcadores} marcadores')
            print(f'    - {base.animais} animais')

    def marcadoresAnalytics(self):
        logger.debug("(dadosAnalyticsController, marcadoresAnalytics)")
        print("MARCADORES: ", Marcador.where().count())
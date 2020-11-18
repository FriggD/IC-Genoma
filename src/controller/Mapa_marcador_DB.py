from ../models/model_app import Marcador, Mapa, Mapa_marcador, session
# Create, create_all, getAll

class Mapa_marcador_DB:
    def __init__(self, session):
        self.session = session
 # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, mapa_marcador):
        try: 
            self.session.add(mapa_marcador)
            self.session.commit()

            return mapa_marcador
        except:
            print("Erro ao fazer o create (mapa_marcador)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr_mapa_marcador):
        try: 
            self.session.add_all(animaisArr_mapa_marcador)
            self.session.commit()

            return mapa_marcador
        except:
            print("Erro ao fazer o createAll (mapa_marcador)!")
            return False

    def getAllAtributos(): # Retorna todos os atributos
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            mapas_marcadores = session.query(Mapa_marcador).all()
            for mapa_marcador in mapas_marcadores:
        print(mapa_marcador)

        except:
            print("Erro ao tentar buscar todos os mapas_marcadores")
            return False

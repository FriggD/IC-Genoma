from src.models.DB_Connection import Mapa_marcador_Schema
# Create, create_all, getAll

class Mapa_marcador_DB:
    def __init__(self, session):
        self.session = session

    # Retorna todos os registros da tabela Mapa_marcador 
    def getAll(self):
        try: 
            return session.query(Mapa_marcador_Schema).all()          

        except:
            print("Erro ao tentar buscar todos os mapas_marcadores")
            return False


    # Recebe uma instância de Mapa_Marcador como parâmetro, e cria o registro dele no banco
    def create(self, mapa_marcador):
        try: 
            self.session.add(mapa_marcador)
            self.session.commit()

            return mapa_marcador
        except:
            print("Erro ao fazer o create (mapa_marcador)!")
            return False


    # Recebe uma lista de Mapa_marcador como parâmetro, e salva todos no banco
    def createAll(self, mapa_marcadorArr):
        try: 
            self.session.add_all(mapa_marcadorArr)
            self.session.commit()

            return mapa_marcadorArr
        except:
            print("Erro ao fazer o createAll (mapa_marcador)!")
            return False



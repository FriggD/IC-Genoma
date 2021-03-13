from src.models.DB_Connection import Animal_mapa_Schema

class Animal_mapa_DB:
    def __init__(self, session):
        self.session = session
    
    # Retorna todos os registros da tabela Animal_mapa
    def getAll(self): 
        try: 
            return session.query(Animal_mapa_Schema).all()

        except:
            print("Erro ao tentar buscar todos os animais_mapas")
            return False
    

    # Recebe uma instância de Animal_mapa_Schema como parâmetro, e cria o registro dele no banco
    def create(self, animal_mapa):
        try: 
            self.session.add(animal_mapa)
            self.session.commit()

            return animal_mapa
        except:
            print("Erro ao fazer o create (animal_mapa)!")
            return False


    # Recebe uma instância de Animal_mapa como parâmetro, e cria o registro dele no banco
    def createAll(self, animal_mapaArr):
        try: 
            self.session.add_all(animal_mapaArr)
            self.session.commit()

            return animal_mapaArr
        except:
            print("Erro ao fazer o createAll (animal_mapa)!")
            return False
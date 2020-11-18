from ../models/model_app import Animal, Mapa, Animal_mapa, session
# Create, create_all, getAll

class Animal_mapa_DB:
    def __init__(self, session):
        self.session = session
 # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, animal_mapa):
        try: 
            self.session.add(animal_mapa)
            self.session.commit()

            return atributo
        except:
            print("Erro ao fazer o create (animal_mapa)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr_animal_mapa):
        try: 
            self.session.add_all(animaisArr_animal_mapa)
            self.session.commit()

            return animal_mapa
        except:
            print("Erro ao fazer o createAll (animal_mapa)!")
            return False

    def getAllAtributos(): # Retorna todos os atributos
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            animais_mapas = session.query(Animal_mapa).all()
            for animal_mapa in animais_mapas:
        print(animal_mapa)

        except:
            print("Erro ao tentar buscar todos os animais_mapas")
            return False

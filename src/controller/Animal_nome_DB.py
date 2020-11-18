from ../models/model_app import Animal, Animal_nome, session

# Create, create_all
class Animal_nome_DB:
    def __init__(self, session):
        self.session = session

    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, animal_nome):
        try: 
            self.session.add(animal_nome)
            self.session.commit()

            return animal_nome
        except:
            print("Erro ao fazer o create (Animal_nome)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr_nome):
        try: 
            self.session.add_all(animaisArr_nome)
            self.session.commit()

            return animal_nome
        except:
            print("Erro ao fazer o createAll (Animal_nome)!")
            return False
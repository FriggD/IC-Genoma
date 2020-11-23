from src.models.DB_Connection import Animal_nome_Schema

class Animal_nome_DB:
    def __init__(self, session):
        self.session = session

    # Recebe uma instância de Animal_nome como parâmetro, e cria o registro dele no banco
    def create(self, animal_nome):
        try: 
            self.session.add(animal_nome)
            self.session.commit()

            return animal_nome
        except:
            print("Erro ao fazer o create (Animal_nome)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animais_nomeArr):
        try: 
            self.session.add_all(animais_nomeArr)
            self.session.commit()

            return animais_nomeArr
        except:
            print("Erro ao fazer o createAll (Animal_nome)!")
            return False